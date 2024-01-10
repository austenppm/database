<?php include 'connect.php'; include 'maindatabase.php' ?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.rtl.min.css">
    <title>Main Database</title>
    <style>
    .scrollable-table {
        max-height: 400px; /* Adjust this value according to your preference */
        overflow-y: auto;
        margin-bottom: 20px;
    }
    </style>
</head>
<body>

<?php
// Render tables for each dataset
renderTable($con, 'Restaurant', ['RestaurantID', 'Username', 'RestaurantName', 'RestaurantDescription', 'CuisineType', 'Price', 'Location', 'UserID']);
?>

</body>
</html>
