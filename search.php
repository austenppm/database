<?php
include 'connect.php';

// Handle the search
$searchTerm = isset($_POST['search']) ? $_POST['search'] : '';
$tableName = $_GET['table'];
$lowercaseTableName = strtolower($tableName);
echo '<a href="' . $lowercaseTableName . '.php" class="btn btn-primary m-2">Home</a>';

// Fetch column names for the query
$columnSql = "SHOW COLUMNS FROM `$tableName`";
$columnResult = mysqli_query($con, $columnSql);
$columns = [];
while($col = mysqli_fetch_assoc($columnResult)) {
    $columns[] = $col['Field'];
}

// Construct search query
$searchQuery = "SELECT * FROM `$tableName` WHERE ";
$searchConditions = [];
foreach ($columns as $column) {
    $searchConditions[] = "`$column` LIKE '%$searchTerm%'";
}
$searchQuery .= implode(' OR ', $searchConditions);

$searchResult = mysqli_query($con, $searchQuery);
?>

<!doctype html>
<html lang="en">
<head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.rtl.min.css">
    <title>Search Results</title>
    <style>
        .highlight { background-color: yellow; }
    </style>
</head>
<body>
    <div class="container my-5">
        <form method="post">
            <div class="form-group mb-3">
                <input type="text" name="search" class="form-control" placeholder="Enter search term" value="<?php echo htmlspecialchars($searchTerm); ?>">
                <button type="submit" class="btn btn-primary mt-3">Search</button>
            </div>
        </form>

        <!-- Display search results -->
        <?php if($searchTerm != ''): ?>
            <table class="table">
                <thead>
                    <tr>
                        <?php foreach($columns as $column): ?>
                            <th><?php echo htmlspecialchars($column); ?></th>
                        <?php endforeach; ?>
                    </tr>
                </thead>
                <tbody>
                    <?php while($row = mysqli_fetch_assoc($searchResult)): ?>
                        <tr>
                            <?php foreach($columns as $column): ?>
                                <td>
                                    <?php 
                                        // Highlight search term in the table cell
                                        echo preg_replace("/($searchTerm)/i", '<span class="highlight">$1</span>', htmlspecialchars($row[$column]));
                                    ?>
                                </td>
                            <?php endforeach; ?>
                        </tr>
                    <?php endwhile; ?>
                </tbody>
            </table>
        <?php endif; ?>
    </div>
</body>
</html>
