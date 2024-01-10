<!DOCTYPE html>
<html>
<head>
    <title>Database Tables</title>
    <style>
        table, th, td {
            border: 1px solid black;
            border-collapse: collapse;
            padding: 5px;
            margin-bottom: 20px;
        }
        body {
            font-family: Arial, sans-serif;
        }
        .scrollable-table {
            height: 300px;
            overflow-y: scroll;
        }
    </style>
</head>
<body>

        <?php
        error_reporting(E_ALL);
        ini_set("display_errors", 1);

        // Function to create a table for each database table
        function createTable($db, $tableName, $columns)
        {
            echo "<h1>" . htmlspecialchars($tableName) . " Table</h1>";
            echo "<div class='scrollable-table'>";
            echo "<table>";
            echo "<thead class='sticky-header'>";
            echo "<tr>";
            foreach ($columns as $column) {
                echo "<th class='sortable' data-column='" . htmlspecialchars($column) . "'>" . htmlspecialchars($column) . "</th>";
            }
            echo "</tr>";
            echo "</thead>";
            echo "<tbody>";
            // Query to retrieve all data from the current table
            $results = $db->query("SELECT * FROM " . $tableName);
            while ($row = $results->fetchArray(SQLITE3_ASSOC)) {
                echo "<tr>";
                foreach ($columns as $column) {
                    echo "<td>" . htmlspecialchars($row[$column]) . "</td>";
                }
                echo "</tr>";
            }
            echo "</tbody>";
            echo "</table>";
            echo "</div>";
            echo "<br>";
            echo "<form method='GET'>";
            echo "<input type='hidden' name='table' value='" . htmlspecialchars($tableName) . "'>";
            echo "<label for='search'>Search:</label>";
            echo "<input type='text' name='search' id='search'>";
            echo "<button type='submit'>Submit</button>";
            echo "</form>";
            echo "<br>";
        }

        // Open database connection
        $db = new SQLite3('restaurant_management.db');

        // Define the columns for each table
        $userColumns = ['UserID', 'Username', 'Password', 'Email', 'PhoneNumber', 'FlagStatus'];
        $adminColumns = ['AdminID', 'SystemSettings', 'SystemMonitoring', 'UserID'];
        $customerColumns = ['CustomerID', 'Username', 'Age', 'Gender', 'Allergies', 'LoyaltyPoints', 'UserID'];
        $restaurantColumns = ['RestaurantID', 'UserID', 'Username', 'RestaurantName', 'RestaurantDescription', 'CuisineType', 'Price', 'Location'];
        $systemDataColumns = ['SystemDataID', 'DataType', 'SystemSettings', 'SystemMonitoring'];
        $reservationColumns = ['ReservationID', 'CustomerID', 'RestaurantID', 'NumberOfPeople', 'Time', 'Allergies', 'Notes', 'PaymentInfo', 'Status'];
        $reviewColumns = ['ReviewID', 'CustomerID', 'RestaurantID', 'ReservationID', 'VerificationStatus', 'Rating', 'Comments'];
        $analyticsColumns = ['AnalyticsID', 'RestaurantID', 'MonthlyTraffic', 'AverageRating', 'PeakTimes'];

        // Create tables for each
        createTable($db, 'User', $userColumns);
        createTable($db, 'Admin', $adminColumns);
        createTable($db, 'Customer', $customerColumns);
        createTable($db, 'Restaurant', $restaurantColumns);
        createTable($db, 'SystemData', $systemDataColumns);
        createTable($db, 'Reservation', $reservationColumns);
        createTable($db, 'Review', $reviewColumns);
        createTable($db, 'Analytics', $analyticsColumns);
        ?>

        <script>
            const searchParams = new URLSearchParams(window.location.search);
            const table = searchParams.get('table');
            const search = searchParams.get('search');
            const orderBy = searchParams.get('order-by');
            const order = searchParams.get('order');

            if (table && search) {
                const tableElement = document.querySelector(`h1:contains(${table})`).nextElementSibling.querySelector('table');
                const columnCount = tableElement.querySelector('thead tr').childElementCount;
                const columnIndex = Array.from(tableElement.querySelectorAll('thead th')).findIndex(th => th.textContent === orderBy);
                const rows = Array.from(tableElement.querySelectorAll('tbody tr'));
                const searchRegex = new RegExp(search, 'i');
                const matchingRow = rows.find(row => Array.from(row.querySelectorAll('td')).some((td, index) => index === columnIndex && searchRegex.test(td.textContent)));
                if (matchingRow) {
                    const rowTop = matchingRow.offsetTop;
                    const tableTop = tableElement.offsetTop;
                    const tableHeight = tableElement.offsetHeight;
                    const rowHeight = matchingRow.offsetHeight;
                    const headerHeight = tableElement.querySelector('thead').offsetHeight;
                    const scrollPosition = rowTop - tableTop - headerHeight - rowHeight;
                    tableElement.parentElement.scrollTop = scrollPosition;
                }
            }

            const sortTable = (table, columnIndex, order) => {
                const rows = Array.from(table.querySelectorAll('tbody tr'));
                rows.sort((a, b) => {
                    const aText = a.querySelectorAll('td')[columnIndex].textContent;
                    const bText = b.querySelectorAll('td')[columnIndex].textContent;
                    if (order === 'asc') {
                        return aText.localeCompare(bText);
                    } else {
                        return bText.localeCompare(aText);
                    }
                });
                rows.forEach(row => table.querySelector('tbody').appendChild(row));
            };

            document.querySelectorAll('.sortable').forEach(th => {
                th.addEventListener('click', () => {
                    const table = th.closest('table');
                    const columnIndex = Array.from(table.querySelectorAll('thead th')).indexOf(th);
                    const order = th.classList.contains('asc') ? 'desc' : 'asc';
                    table.querySelectorAll('thead th').forEach(th => th.classList.remove('asc', 'desc'));
                    th.classList.add(order);
                    sortTable(table, columnIndex, order);
                });
            });

            document.querySelectorAll('.scrollable-table').forEach(table => {
                table.addEventListener('scroll', () => {
                    const header = table.querySelector('thead');
                    const top = table.getBoundingClientRect().top;
                    if (top < 0) {
                        header.classList.add('sticky');
                    } else {
                        header.classList.remove('sticky');
                    }
                });
            });
        </script>

        <style>
            table, th, td {
                border: 1px solid black;
                border-collapse: collapse;
                padding: 5px;
                margin-bottom: 20px;
            }

            body {
                font-family: Arial, sans-serif;
            }

            .scrollable-table {
                height: 300px;
                overflow-y: scroll;
            }

            .sticky-header {
                position: sticky;
                top: 0;
                background-color: white;
            }

            .sticky-header th {
                position: sticky;
                top: 0;
                z-index: 1;
            }

            .sticky-header.sticky th {
                background-color: white;
            }

            .sortable {
                cursor: pointer;
            }

            .asc::after {
                content: ' ▲';
            }

            .desc::after {
                content: ' ▼';
            }
        </style>
        <script>
        // Search functionality
        // Assuming you want to search across all columns, you need to modify the JavaScript to iterate through each cell of each row.
        if (table && search) {
            const tableElement = document.querySelector(`h1:contains(${table}) + .scrollable-table table`);
            if (tableElement) {
                const rows = Array.from(tableElement.querySelectorAll('tbody tr'));
                let found = false;
                for (let row of rows) {
                    let cells = row.querySelectorAll('td');
                    for (let cell of cells) {
                        if (cell.textContent.includes(search)) {
                            const rowTop = row.offsetTop;
                            tableElement.parentElement.scrollTop = rowTop - tableElement.parentElement.offsetTop;
                            found = true;
                            break;
                        }
                    }
                    if (found) break;
                }
            }
        }

        // Sort functionality integrated into column headers
        document.querySelectorAll('.sortable').forEach(th => {
            th.addEventListener('click', () => {
                const table = th.closest('table');
                const columnIndex = Array.from(table.querySelectorAll('thead th')).indexOf(th);
                const currentOrder = th.getAttribute('data-order') || 'asc';
                const newOrder = currentOrder === 'asc' ? 'desc' : 'asc';
                th.setAttribute('data-order', newOrder);
                th.classList.toggle('asc', newOrder === 'asc');
                th.classList.toggle('desc', newOrder === 'desc');
                sortTable(table, columnIndex, newOrder);
            });
        });

        // Update your style to include the sorting arrows
            .sortable.asc::after {
                content: ' \\25B2'; /* Unicode for up-pointing triangle */
            }

            .sortable.desc::after {
                content: ' \\25BC'; /* Unicode for down-pointing triangle */
}</script>
    </body>
    </html>
