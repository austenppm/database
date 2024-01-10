<?php

$con=new mysqli('localhost', 'root','','restaurant_database');

if(!$con){
    die(mysqli_error($con));
}

?>