<?php
include 'connect.php';

$tableName = $_GET['table'];
$lowercaseTableName = strtolower($tableName);
echo '<a href="' . $lowercaseTableName . '.php" class="btn btn-primary m-2">Home</a>';

$id = $_GET['updateid'];

// Construct primary key column name
$primaryKeyColumn = $tableName . 'ID';

// Fetch data for the record to be updated
$dataSql = "SELECT * FROM `$tableName` WHERE `$primaryKeyColumn` = '$id'";
$dataResult = mysqli_query($con, $dataSql);
$dataRow = mysqli_fetch_assoc($dataResult);

// Update record
if(isset($_POST['update'])) {
    $updateParts = [];
    foreach($_POST as $key => $value) {
        if($key != 'update') {
            $updateParts[] = "`$key` = '".mysqli_real_escape_string($con, $value)."'";
        }
    }
    $updateSql = "UPDATE `$tableName` SET ".implode(', ', $updateParts)." WHERE `$primaryKeyColumn` = '$id'";
    $updateResult = mysqli_query($con, $updateSql);
    $lowertablename = strtolower($tableName);
    if($updateResult) {
        header("location:$lowertablename.php"); // Redirect as needed
    } else {
        die(mysqli_error($con));
    }
}
?>

<!doctype html>
<html lang="en">
<head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.rtl.min.css">
    <title>Update Record</title>
</head>
<body>
    <div class="container my-5">
        <form method="post">
            <?php
            if($dataRow) {
                foreach($dataRow as $key => $value) {
                    if($key != $primaryKeyColumn) {
                        echo '<div class="form-group mb-3">';
                        echo '<label>'.ucfirst($key).'</label>';
                        echo '<input type="text" class="form-control" name="'.$key.'" value="'.$value.'">';
                        echo '</div>';
                    }
                }
            }
            ?>
            <button type="submit" class="btn btn-primary" name="update">Update</button>
        </form>
    </div>
</body>
</html>
