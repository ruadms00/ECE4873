<?php
   include('config.php');
   session_start();
   
   $user_id = $_SESSION['login_user'];
   
   $ses_sql = mysqli_query($conn,"SELECT * FROM users WHERE userid = '$user_id' ");
   
   $row = mysqli_fetch_array($ses_sql,MYSQLI_ASSOC);
   
   if(!isset($_SESSION['login_user'])){
      header("location:index.php");
      die();
   }
?>
