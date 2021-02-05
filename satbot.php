
<html>
<style>
table, th, td {
  border: 1px solid black;
  border-collapse: collapse;
}
</style>
<body>

<?php


$mysqli = new mysqli("localhost","satbot","Yega2828","satbot");
// Check connection
if ($mysqli -> connect_errno) {
  echo "Failed to connect to MySQL: " . $mysqli -> connect_error;
  exit();
}

$sql="SELECT * FROM items ORDER BY date_added";
// $result=mysqli_query($mysqli,$sql);
// Fetch all


// while ($row = $result -> fetch_row()) {
//  printf ("%s %s %s %s %s %s \n", $row[0],$row[1],$row[2],$row[3],$row[4],$row[5]);
// }
echo '<table border="0" cellspacing="2" cellpadding="2" border="1">
      <tr>
          <td> <font face="Arial">ID</font> </td>
          <td> <font face="Arial">USERNAME</font> </td>
          <td> <font face="Arial">ITEMNAME</font> </td>
          <td> <font face="Arial">PICTURE</font> </td>
          <td> <font face="Arial">LOCATION</font> </td>
          <td> <font face="Arial">STATUS</font> </td>
          <td> <font face="Arial">DATE ADDED</font> </td>
          <td> <font face="Arial">APPROVEMENT</font> </td>
          <td> <font face="Arial">NOTE</font> </td>
      </tr>';

if ($result = $mysqli->query($sql)) {
    while ($row = $result->fetch_assoc()) {
        $field1name = $row['id'];
        $field2name = $row['username'];
        $field3name = $row['itemname'];
        $field4name = $row['picture'];
        $field5name = $row['location'];
        $field6name = $row['status'];
        $field7name = $row['date_added'];
        $field8name = $row['NOTE'];

        echo '<tr >
                  <td>'.$field1name.'</td>
                  <td>'.$field2name.'</td>
                  <td>'.$field3name.'</td>
                  <td><image width="50" height="50"  src="images/'.$field4name.'"></td>
                  <td>'.$field5name.'</td>
                  <td>'.$field6name.'</td>
                  <td>'.$field7name.'</td>
                  <td><a href=/approve.php?id='.$field1name.'> ONAYLA</a>//<a href=/deapprove.php?='.$field1name.'> ONAYLAMA</a></td>
                  <td></td>
                  <td>'.$field8name.'</td>

              </tr>';
    }
    $result->free();
}





 ?>
</body>
</html>
