<?php
   include('session.php');
?>

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">

    <link href='https://fonts.googleapis.com/css?family=Strait' rel='stylesheet'>
    <style type="text/css">
    <!--
    body {
  	margin: 0;
      color:#f0f0f0;
      font-family: 'Strait';font-size: 22px;
      background-color:#191919;
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
    padding: 20px;
    margin: 8px 0;
    border: none;
    cursor: pointer;
    width: 100%;
  }
  
  .button:hover {
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

.btn-group button {
background-color: #262626; /* Green background */
color: white; /* White text */
cursor: pointer; /* Pointer/hand icon */
float: left; /* Float the buttons side by side */
}

.btn-group:after {
content: "";
clear: both;
display: table;
}
.btn-group button:not(:last-child) {
border-right: none; /* Prevent double borders */
}

/* Add a background color on hover */
.btn-group button:hover:not(.active) {
  background-color: #323232;
  color: white;
}
.btn-group button:hover:active {
  background-color: #262626;
  color: white;
}
.rect {
background-color: #262626;
color: white;
padding: 15px ;
margin: 15% 25%;
border: 2px solid black;
cursor: pointer;
height: 400px;
width: 40%;
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
  <a class="active">Users</a>
  <a href="ControlQueue.php">Queue</a>
  <a href="ControlSettings.php">Settings</a>
</div>
<div class="content">
  <h1>
<form action="" method="post">
    USERS
    <button type="button" class="cancelbtn">Logout</button>
</form>
    </h1>
<form action="" method="post">
<div class = "rect">
    <img src="https://i.scdn.co/image/966ade7a8c43b72faa53822b74a899c675aaafee" alt="image" style="padding-left:5%;width:90%;height:75%;margin-bottom:0%;">
    <div class = "btn-group" style = "width:100%; margin-bottom:0%"> 
     
        <button type="button" style="width:20%; "><i class="material-icons">skip_previous</i></button>
        <button type="button" style="width:20%; "><i class="material-icons">pause</i></button>
        <button type="button" style="width:20%;"><i class="material-icons">play_arrow</i></button>
        <button type="button" style="width:20%;"><i class="material-icons">shuffle</i></button>
        <button type="button" style="width:20%;"><i class="material-icons">skip_next</i></button>

    </div>
</div>
    
</form>
	   </div>
  </body>
</html>

