<?php
include 'connect.php';

if(isset($_GET['deleteid']) && isset($_GET['table'])) {
    $id = $_GET['deleteid'];
    $tableName = $_GET['table'];

    // Construct primary key column name
    $primaryKeyColumn = $tableName . 'ID';

    // SQL query to delete the record
    $sql = "DELETE FROM `$tableName` WHERE `$primaryKeyColumn` = '$id'";
    $result = mysqli_query($con, $sql);
    if($result){
        $lowertablename = strtolower($tableName);
        header("location:$lowertablename.php"); // Redirect to the table's page
    } else {
        die(mysqli_error($con));
    }
}
?>
