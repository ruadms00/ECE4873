<?php
   include('session.php');
?>

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Boombox</title>
    
    <link href='https://fonts.googleapis.com/css?family=Strait' rel='stylesheet'>
    <style type="text/css">
    <!--
    body {
  	margin: 0;
      color:#0080FF;
      font-family: 'Strait';font-size: 22px;
      background-color:#4B4B4B;
    }
    a  { color:#0000FF; }

	h1 {
	width:100%;
	   margin:10px;
	   text-align: center;
	   float:right;
	}
	

  input[type=text], input[type=password] {
    width: 100%;
    padding: 12px 20px;
    margin: 8px 0;
    display: inline-block;
    border: 1px solid #ccc;
    box-sizing: border-box;
  }
  
  button {
    background-color: #4CAF50;
    color: white;
    padding: 14px 20px;
    margin: 8px 0;
    border: none;
    cursor: pointer;
    width: 100%;
  }
  
  button:hover {
    opacity: 0.8;
  }
 
 div.content {
  margin-left: 200px;
  padding: 1px 16px;
  height: 1000px;
} 
  
.sidebar {
  margin: 0;
  padding: 0;
  width: 200px;
  background-color: #f1f1f1;
  position: fixed;
  height: 100%;
  overflow: auto;
  float:left;
}


.sidebar a {
  display: block;
  color: black;
  padding: 16px;
  text-decoration: none;
}
 
.sidebar a.active {
  background-color: #4CAF50;
  color: white;
}

.sidebar a:hover:not(.active) {
  background-color: #555;
  color: white;
}

  
  .cancelbtn {
    width: auto;
    padding: 10px 20px;
    background-color: #f44336;
	float:right;
  }
  
  .left {
    padding: 16px;
	float:left;
	width:50%;
  }
  
  .right {
    padding: 16px;
  }
  
  
  /* Change styles for span and cancel button on extra small screens */
  @media screen and (max-width: 300px) {
    span.psw {
       display: block;
       float: none;
    }
    .cancelbtn {
       width: 100%;
    }
  }
  
@media screen and (max-width: 700px) {
  .sidebar {
    width: 100%;
    height: auto;
    position: relative;
  }
  .sidebar a {float: left;}
  div.content {margin-left: 0;}
}

@media screen and (max-width: 400px) {
  .sidebar a {
    text-align: center;
    float: none;
  }
}
    -->
    </style>
    <!--[if IE]>
    <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
    <![endif]-->
  </head>
  <body>

<div class="sidebar">
  <a href="ControlAdd.php">Add Music</a>
  <a href="ControlUsers.php">Users</a>
  <a href="ControlQueue.php">Queue</a>
  <a class="active">Settings</a>
</div>
<div class="content">
  <h1>
  SETTINGS
    </h1>
<form action="" method="post">
  <div class="left">
    <button type="button" class="cancelbtn">Logout</button>
  </div>
  <div class="right">
 <label>
 OR SCAN QR CODE HERE
 </label>
  </div>
</form>
	   </div>
  </body>
</html>
