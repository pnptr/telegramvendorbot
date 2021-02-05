#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=W0613, C0116
# type: ignore[union-attr]



import logging
import mysql.connector
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

ALSAT,PNAME, PHOTO, LOCATION = range(4)

vals=[]

def start(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['Al', 'Sat']]

    update.message.reply_text(
        'Merhaba! Ben bir alım-satım botuyum. '
        '/iptal yazarak işlemi durdurabilirsiniz.\n\n'
        'Almak mı yoksa satmak mı istiyorsunuz?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return PNAME

def pname(update: Update,context:CallbackContext)->int:
    user = update.message.from_user
    userid = user.id
    vals.extend([userid,user.first_name])
    update.message.reply_text(
        'Lütfen ürünün ismini yazınız. ')
    return ALSAT


def alsat(update: Update, context: CallbackContext) -> int:

    user = update.message.from_user
    productname = update.message.text
    vals.append(productname)
    logger.info("Alım-Satım %s: %s", user.first_name, productname)
    update.message.reply_text(
        'Lütfen ürünün fotoğrafını yükleyiniz, '
        'eklemek istemiyorsanız /ilerle yazarak bir sonraki aşamaya geçebilirsiniz.',
        reply_markup=ReplyKeyboardRemove(),
    )

    return PHOTO


def photo(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    userid = user.id
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('images/'+str(userid)+vals[2]+'_user_photo.jpg')
    vals.append(str(userid)+vals[2]+'_user_photo.jpg')
    vals.append('0')
    logger.info("Photo of %s: %s", user.first_name, str(userid)+'user_photo.jpg')
    update.message.reply_text(
        'Lütfen lokasyonunuzu il ilçe olarak belirtiniz'
    )

    return LOCATION


def skip_photo(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s did not send a photo.", user.first_name)
    update.message.reply_text(
        'I bet you look great! Now, send me your location please, ' 'or send /skip.'
    )

    return LOCATION


def location(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    user_location = update.message.text
    vals.append(user_location)
    logger.info(
        "Location of %s: %s ", user.first_name, user_location
    )
    mydb = mysql.connector.connect(
        host="localhost",
        user="satbot",
        password="Yega2828",
        database="satbot",
	auth_plugin="mysql_native_password"
        )
    sql="INSERT INTO items(userid,username,itemname,picture,status,location) values (%s,%s,%s,%s,%s,%s)"
    satbot_cursor=mydb.cursor()
    val=("1","1","1","1","1","1")
    satbot_cursor.execute(sql,vals)
    mydb.commit()
    print(satbot_cursor.rowcount, "record inserted.")
    update.message.reply_text(
        'ilan talebiniz başarıyla alındı onay sürecindesiniz.'
    )
    print(vals)
    return ConversationHandler.END


def skip_location(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s did not send a location.", user.first_name)
    update.message.reply_text(
        'Lokasyonunuzu lütfen belirtiniz'
    )

    return LOCATION




def cancel(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Görüşmek üzere teşekkürler.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("1332060002:AAFUewcS-EPpF8RsbwuOuk7b468MqUSSxEs", use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('alsat', start,filters=Filters.private)],
        states={
            ALSAT: [MessageHandler(Filters.text, alsat)],
            PNAME: [MessageHandler(Filters.text, pname)],
            PHOTO: [MessageHandler(Filters.photo, photo), CommandHandler('ilerle', skip_photo)],
            LOCATION: [MessageHandler(Filters.text, location),CommandHandler('ilerle', skip_location)],
            # BIO: [MessageHandler(Filters.text & ~Filters.command, bio)],
        },
        fallbacks=[CommandHandler('iptal', cancel,filters=Filters.private)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
