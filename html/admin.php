<?php
   include('config.php');
   session_start();
   
   $user_id = $_SESSION['login_user'];
   
   $ses_sql = mysqli_query($conn,"SELECT * FROM users WHERE userid = '$user_id' ");
   
   $row = mysqli_fetch_array($ses_sql,MYSQLI_ASSOC);
   
   if (!$row["is_owner"]) {
           ob_start();
      header("Location: index.php");
      die();
   }
   
   if(!isset($_SESSION['login_user'])){
           ob_start();
      header("Location: index.php");
      die();
   }
?>
