import sqlite3
import mysql.connector

# Connect to SQLite database
sqlite_conn = sqlite3.connect('restaurant_management.db')
sqlite_cursor = sqlite_conn.cursor()

# Connect to MySQL database
mysql_conn = mysql.connector.connect(
    host='localhost',
    user='austenppm',
    password='Bce9cdefbdf5',
    database='restaurant_management'
)
mysql_cursor = mysql_conn.cursor()

# Retrieve schema from SQLite database
sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = sqlite_cursor.fetchall()
for table_name in tables:
    table_name = table_name[0]
    sqlite_cursor.execute(f"PRAGMA table_info({table_name})")
    info = sqlite_cursor.fetchall()
    create_table_query = f"CREATE TABLE {table_name} ("
    for column in info:
        column_name = column[1]
        data_type = column[2]
        create_table_query += f"{column_name} {data_type}, "
    create_table_query = create_table_query[:-2] + ")"
    mysql_cursor.execute(create_table_query)

    # Retrieve data from SQLite table and insert into MySQL table
    sqlite_cursor.execute(f"SELECT * FROM {table_name}")
    rows = sqlite_cursor.fetchall()
    for row in rows:
        insert_query = f"INSERT INTO {table_name} VALUES ("
        for value in row:
            if isinstance(value, str):
                insert_query += f"'{value}', "
            else:
                insert_query += f"{value}, "
        insert_query = insert_query[:-2] + ")"
        mysql_cursor.execute(insert_query)

# Commit changes and close connections
mysql_conn.commit()
mysql_cursor.close()
mysql_conn.close()
sqlite_cursor.close()
sqlite_conn.close()
