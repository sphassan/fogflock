<!DOCTYPE html>
<html lang="en">
    <head>
    <style type="text/css">
    html,body {
    background: url("bg.jpg") no-repeat center center fixed;
    -webkit-background-size: cover; /* For WebKit*/
    -moz-background-size: cover;    /* Mozilla*/
    -o-background-size: cover;      /* Opera*/
    background-size: cover;         /* Generic*/
    }
    </style>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
    </head>
    <body>
      <nav class="navbar navbar-inverse">
        <center><a href="http://fogflock.com"><img src="fogflock_logo.png" height=64px width=171px></a></center>
      </nav>

        <div class="container-fluid center-block" style="width:100%">
        <div class="row center-block" style="max-width:1200px">
        </br>
        <div style="height:600px">
        <svg class="box" viewbox="0 0 500 250" id="graphDiv" style="height:600px"></svg>
        <script src = "scripts/jquery.min.js"></script>
        <script src = "scripts/vivagraph.min.js"></script>
        <script id="test" src = "data.json"></script>
        <script src = "scripts/main.js"></script>
      </div>
        </br>
          <?php
          $result = json_decode(file_get_contents("http://fogflock.com:8080/hello?text=".urlencode($_GET['users']), false));
          foreach($result AS $mydata)
          {
              if($mydata->level == 0)
              {
              echo"<div class=\"col-xs-12 col-sm-6 col-md-4 col-lg-3\">";
              echo "<a href=\"" . $mydata->permalink_url . "\" class=\"btn btn-default btn-block\" \"><img src=\"".str_replace("large","t500x500",$mydata->avatar_url)."\" height=100% width=100%></br><h4>".$mydata->sc_display_name."</h4></a></br>";
              echo"</div>";
              }
              else {
                echo"<div class=\"col-xs-12 col-sm-6 col-md-4 col-lg-3\">";
                echo "<a href=\"" . $mydata->permalink_url . "\" class=\"btn btn-success btn-block\" \"><img src=\"".str_replace("large","t500x500",$mydata->avatar_url)."\" height=100% width=100%></br><h4>".$mydata->sc_display_name."</h4></a></br>";
                echo"</div>";
              }
          }
          ?>
      </div>
    </div>
  </body>
</html>
