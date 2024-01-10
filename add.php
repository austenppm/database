<?php
include 'connect.php';

$tableName = $_GET['table'];
$lowercaseTableName = strtolower($tableName);
$primaryKeyColumn = $tableName . 'ID';

// Fetch column names from the table
$columnSql = "SHOW COLUMNS FROM `$tableName`";
$columnResult = mysqli_query($con, $columnSql);
$columns = [];
while($col = mysqli_fetch_assoc($columnResult)) {
    $columns[] = $col['Field'];
}

// Handling form submission
if(isset($_POST['submit'])) {
    // Get the highest current ID
    // Get the highest current ID
    $idSql = "SELECT MAX($primaryKeyColumn) as maxId FROM `$tableName`";
    $idResult = mysqli_query($con, $idSql);
    $idRow = mysqli_fetch_assoc($idResult);
    $maxId = $idRow['maxId'];

    // Regular expression to separate the prefix and the numeric part
    if (preg_match('/(^[A-Z_]+)([0-9]+)$/', $maxId, $matches)) {
        $prefix = $matches[1];
        $numericPart = $matches[2];
        
        // Increment the numeric part
        $newNumericPart = str_pad(intval($numericPart) + 1, strlen($numericPart), '0', STR_PAD_LEFT);
        $newId = $prefix . $newNumericPart;
    } else {
        die("Invalid ID format");
    }
    // Prepare SQL for insertion
    $insertValues = ["'$newId'"];
    foreach($columns as $column) {
        if($column != $primaryKeyColumn) {
            $insertValues[] = "'".mysqli_real_escape_string($con, $_POST[$column])."'";
        }
    }
    $sql = "INSERT INTO `$tableName` (" . implode(', ', $columns) . ") VALUES (" . implode(', ', $insertValues) . ")";
    $result = mysqli_query($con, $sql);
    if($result) {
        $lowertablename = strtolower($tableName);
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
    <title>Add New Record</title>
</head>
<body>
    <div class="container my-5">
        <form method="post">
            <?php
            echo '<a href="' . $lowercaseTableName . '.php" class="btn btn-primary m-2">Home</a>';
            foreach($columns as $column) {
                if($column != $primaryKeyColumn) {
                    $placeholder = "Enter " . str_replace('_', ' ', strtolower($column));
                    echo '<div class="form-group mb-3">';
                    echo '<label>'.ucfirst(str_replace('_', ' ', $column)).'</label>';
                    echo '<input type="text" class="form-control" name="'.$column.'" placeholder="'.$placeholder.'" autocomplete="off">';
                    echo '</div>';
                }
            }
            ?>
            <button type="submit" class="btn btn-primary" name="submit">Submit</button>
        </form>
    </div>
</body>
</html>
