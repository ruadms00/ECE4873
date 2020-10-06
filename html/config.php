<?php
    $servername = "localhost";
    $username = "pi";
    $password = "treblejackets";
    $dbname = "treblejackets";
 
/* Attempt to connect to MySQL database */
    $conn = mysqli_connect($servername, $username, $password, $dbname);
 
// Check connection
if($conn === false){
    die("ERROR: Could not connect. " . mysqli_connect_error());
}
?>
