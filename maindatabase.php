<?php include 'connect.php'; ?>

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
<div class="container mt-4">
    <h1>Main Tables</h1>
    <div class="my-4">
        <a href="user.php" class="btn btn-primary m-2">User</a>
        <a href="admin.php" class="btn btn-primary m-2">Admin</a>
        <a href="customer.php" class="btn btn-primary m-2">Customer</a>
        <a href="restaurant.php" class="btn btn-primary m-2">Restaurant</a>
        <a href="systemdata.php" class="btn btn-primary m-2">System Data</a>
        <a href="reservation.php" class="btn btn-primary m-2">Reservation</a>
        <a href="review.php" class="btn btn-primary m-2">Review</a>
        <a href="analytics.php" class="btn btn-primary m-2">Analytics</a>
    </div>
</div>
<?php
function renderTable($db, $tableName, $columns) {
    $query = "SELECT * FROM `$tableName`";
    $result = mysqli_query($db, $query);

    if ($result) {
        echo '<div class="container mt-4">';
        echo '<h2>'.ucfirst($tableName).'</h2>';

        // Row for search and add button
        echo '<div class="row mb-3">';

        // Column for search
        echo '<div class="col-md-8">';
        echo '<div class="input-group">';
        echo '<form method="post" action="search.php?table='.$tableName.'" class="w-100 d-flex">'; // Modify the action attribute
        echo '<input type="text" placeholder="Search Data" name="search" class="form-control">';
        echo '<button class="btn btn-dark" type="submit" name="submit">Search</button>';
        echo '</form>';
        echo '</div>';        
        echo '</div>'; // Close column for search


        // Column for add button
        echo '<div class="col-md-4 d-flex align-items-center">';
        echo '<a href="add.php?table='.$tableName.'" class="btn btn-primary text-light">Add '.ucfirst($tableName).' Entry</a>';
        echo '</div>'; // Close column for add button

        echo '</div>'; // Close row

        // Table
        echo '<div class="scrollable-table"><table id="'.$tableName.'Table" class="table table-striped">';
        echo '<thead class="thead-dark"><tr>';

        foreach ($columns as $col) {
            echo '<th scope="col">'.$col.'</th>';
        }

        echo '<th scope="col">Operations</th>';
        echo '</tr></thead>';
        echo '<tbody>';
        while ($row = mysqli_fetch_assoc($result)) {
            echo '<tr>';

            foreach ($columns as $col) {
                echo '<td>'.$row[$col].'</td>';
            }

            $idCol = $columns[0];
            echo '<td>
                    <button class="btn btn-primary"><a href="update.php?table='.$tableName.'&updateid='.$row[$idCol].'" class="text-light">Update</a></button>
                    <button class="btn btn-danger"><a href="delete.php?table='.$tableName.'&deleteid='.$row[$idCol].'" class="text-light">Delete</a></button>
                  </td>';
            echo '</tr>';
        }

        echo '</tbody></table></div>';
    } else {
        echo 'Error: '.mysqli_error($db);
    }
}


// Render tables for each dataset
// renderTable($con, 'User', ['UserID', 'Username', 'Email', 'PhoneNumber', 'Password', 'FlagStatus']);
// renderTable($con, 'Admin', ['AdminID', 'SystemSettings', 'SystemMonitoring', 'UserID']);
// renderTable($con, 'Customer', ['CustomerID', 'Age', 'Gender', 'Allergies']);
// renderTable($con, 'Restaurant', ['RestaurantID', 'RestaurantDescription', 'CuisineType', 'Price', 'Location']);
// renderTable($con, 'SystemData', ['SystemDataID', 'DataType', 'Authorization', 'FlagStatus', 'AdminID']);
// renderTable($con, 'Reservation', ['ReservationID', 'CustomerID', 'RestaurantID', 'NumberOfPeople', 'Time', 'Allergies', 'Notes', 'PaymentInfo', 'Status']);
// renderTable($con, 'Review', ['ReviewID', 'CustomerID', 'RestaurantID', 'ReservationID', 'VerificationStatus', 'Rating', 'Comments']);
// renderTable($con, 'LoyaltyPoints', ['CustomerID', 'Points']);
// renderTable($con, 'Analytics', ['AnalyticsID', 'RestaurantID', 'MonthlyTraffic', 'AverageRating', 'PeakTimes']);

?>

</body>
</html>
