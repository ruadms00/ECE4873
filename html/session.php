<?php
   include('config.php');
   session_start();
   
   if(!isset($_SESSION['login_user'])){
           ob_start();
      header("location:index.php");
      die();
   }
?>
