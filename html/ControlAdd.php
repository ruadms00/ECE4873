<?php
   include('session.php');
?>

<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Boombox</title>
    
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
  
.rect {
    background-color: #262626;
    color: white;
    padding: 15px ;
    margin-left: 25%;
    margin-top: 25%;
    border: 2px solid black;
    cursor: pointer;
    height: 300px;
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
  <a class="active">Add Music</a>
  <a href="ControlUsers.php">Users</a>
  <a href="ControlQueue.php">Queue</a>
  <a href="ControlSettings.php">Settings</a>
</div>
<div class="content">
    <h1>
    <form action="" method="post">
    ADD MUSIC <?php echo strtoupper($user_id); ?>
    <a href="logout.php"><button type="button" class="cancelbtn">Logout</button></a>
</form>
    </h1>
    <form action="" method="post"></form>
    <div class = "rect" style = "margin-top: 10%;" >    
        
        <div  >
            <label>Song</label>
            <input type="text">
        </div>
        <div >
            <label>Artist</label>
            <input type="text">
        </div>
        <div>
            <button type = "button" style = "width:45%; font-size: 15px">Add</button>
            <button type = "button" style = "width:45%;margin-left:5%; font-size: 15px">Remove</button>
        </div>
    </div>
</div>
  </body>
</html>
