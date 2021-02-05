<?php
$itemid=$_GET["id"];

$mysqli = new mysqli("localhost","satbot","Yega2828","satbot");
// Check connection
if ($mysqli -> connect_errno) {
  echo "Failed to connect to MySQL: " . $mysqli -> connect_error;
  exit();
}


$sql = "UPDATE items SET status='-1' WHERE id='$itemid'";

if ($mysqli->query($sql) === TRUE) {
  echo "Record updated successfully";
} else {
  echo "Error updating record: " . $mysqli->error;
}

$mysqli->close();


 ?>
