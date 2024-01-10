import sqlite3

def init_db():
    conn = sqlite3.connect('restaurant_management.db')
    c = conn.cursor()

# DELIMITER $$
# CREATE TRIGGER tg_tableName_insert
# BEFORE INSERT ON tableName
# FOR EACH ROW
# BEGIN
#   INSERT INTO tableName_seq VALUES (NULL);
#   SET NEW.id = CONCAT('IDC', LPAD(LAST_INSERT_ID(), 8, '0'));
# END$$
# DELIMITER ;

# CREATE TABLE tableName_seq
# (
#   id INT NOT NULL AUTO_INCREMENT PRIMARY KEY
# );
# CREATE TABLE tableName
# (
#   id VARCHAR(11) NOT NULL PRIMARY KEY DEFAULT '0'
# );
    # Create User table
    c.execute("""
    CREATE TABLE IF NOT EXISTS User (
        UserID TEXT PRIMARY KEY,
        Username TEXT NOT NULL,
        Password TEXT NOT NULL,
        Email TEXT UNIQUE NOT NULL,
        PhoneNumber TEXT,
        FlagStatus TEXT
    );
    """)

    # Create Admin table
    c.execute("""
    CREATE TABLE IF NOT EXISTS Admin (
        AdminID TEXT PRIMARY KEY,
        SystemSettings TEXT,
        SystemMonitoring TEXT,
        UserID TEXT,
        FOREIGN KEY (UserID) REFERENCES User(UserID)
    );
    """)

    # Create Customer table
    c.execute("""
    CREATE TABLE IF NOT EXISTS Customer (
        CustomerID TEXT PRIMARY KEY,
        Username TEXT,
        Age INTEGER,
        Gender TEXT,
        Allergies TEXT,
        UserID TEXT,
        LoyaltyPoints INTEGER,
        FOREIGN KEY (UserID) REFERENCES User(UserID),
        FOREIGN KEY (Username) REFERENCES User(Username)
    );
    """)

    # Create Restaurant table
    c.execute("""
    CREATE TABLE IF NOT EXISTS Restaurant (
        RestaurantID TEXT PRIMARY KEY,
        Username TEXT,
        RestaurantName TEXT NOT NULL,
        RestaurantDescription TEXT,
        CuisineType TEXT,
        Price REAL,
        Location TEXT,
        UserID TEXT,
        FOREIGN KEY (UserID) REFERENCES User(UserID),
        FOREIGN KEY (Username) REFERENCES User(Username)
    );
    """)

    # Create SystemData table
    c.execute("""
    CREATE TABLE IF NOT EXISTS SystemData (
        SystemDataID TEXT PRIMARY KEY,
        DataType TEXT,
        SystemSettings TEXT,
        SystemMonitoring TEXT
        );
    """)

    # Create Reservation table
    c.execute("""
    CREATE TABLE IF NOT EXISTS Reservation (
        ReservationID TEXT PRIMARY KEY,
        CustomerID TEXT,
        RestaurantID TEXT,
        NumberOfPeople INTEGER,
        Time TEXT,
        Allergies TEXT,
        Notes TEXT,
        PaymentInfo TEXT,
        Status TEXT,
        FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
        FOREIGN KEY (RestaurantID) REFERENCES Restaurant(RestaurantID)
    );
    """)

    # Create Review table
    c.execute("""
    CREATE TABLE IF NOT EXISTS Review (
        ReviewID TEXT PRIMARY KEY,
        CustomerID TEXT,
        RestaurantID TEXT,
        ReservationID INTEGER,
        VerificationStatus TEXT,
        Rating REAL,
        Comments TEXT,
        FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID),
        FOREIGN KEY (RestaurantID) REFERENCES Restaurant(RestaurantID),
        FOREIGN KEY (ReservationID) REFERENCES Reservation(ReservationID)
    );
    """)

    # Create Analytics table
    c.execute("""
    CREATE TABLE IF NOT EXISTS Analytics (
        AnalyticsID TEXT PRIMARY KEY,
        RestaurantID TEXT,
        MonthlyTraffic INTEGER,
        AverageRating REAL,
        PeakTimes TEXT,
        FOREIGN KEY (RestaurantID) REFERENCES Restaurant(RestaurantID)
    );
    """)

def show_limit(table, ascend_or_descend, limit):
    conn = sqlite3.connect('restaurant_management.db')
    c = conn.cursor()
    c.execute("SELECT * FROM {} ORDER BY rowid {} LIMIT {}".format(table, ascend_or_descend, limit))
    items = c.fetchall()
    for item in items:
        print(item) 
    conn.commit()
    conn.close()
        
def delete_table(table):
    conn = sqlite3.connect('restaurant_management.db')
    c = conn.cursor()
    c.execute("DROP TABLE {}".format(table))
    conn.commit()
    conn.close()    
    
def delete_alltablesandrelations():
    conn = sqlite3.connect('restaurant_management.db')
    c = conn.cursor()
    tables = ["User", "Admin", "Customer", "Restaurant", "SystemData", "Reservation", "Review", "Analytics"]
    for table in tables:
        try:
            c.execute(f"DROP TABLE {table}")
        except sqlite3.OperationalError:
            # If the table does not exist, it will raise an error. We can catch it and continue.
            pass

    conn.commit()
    conn.close()

def show_all_first_x(x):
    conn = sqlite3.connect('restaurant_management.db')
    c = conn.cursor()
    # List of all table names to query
    tables = ['User', 'Admin', 'Customer', 'Restaurant', 'SystemData', 'Reservation', 'Review', 'Analytics']
    for table in tables:
        print(f"First {x} items from {table} table:")
        c.execute(f"SELECT * FROM {table} LIMIT {x}")
        items = c.fetchall()
        for item in items:
            print(item)
        print("\n")  # Adds a new line for better readability between tables
    conn.close()  # No commit needed as we are not making changes to the database

def show_all_last_10():
    conn = sqlite3.connect('restaurant_management.db')
    c = conn.cursor()
    # List of all table names to query
    tables = ['User', 'Admin', 'Customer', 'Restaurant', 'SystemData', 'Reservation', 'Review', 'Analytics']
    for table in tables:
        print(f"First 10 items from {table} table:")
        c.execute(f"SELECT rowid, * FROM {table} ORDER BY rowid DESC LIMIT 10")
        items = c.fetchall()
        for item in items:
            print(item)
        print("\n")  # Adds a new line for better readability between tables
    conn.close()  # No commit needed as we are not making changes to the database