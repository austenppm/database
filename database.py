import sqlite3

conn = sqlite3.connect('customer.db')

# conn = sqlite3.connect(':memory:')
# create a cursor
c = conn.cursor()
# Create a Table
# c.execute("""CREATE TABLE customers (
#     first_name text,
#     last_name text, 
#     email text
# )""")
#Create a Table
# NULL
# INTEGER
# REAL
# TEXT
# BLOB
# DATATYPE

def show_all():
    conn = sqlite3.connect('customer.db')
    c = conn.cursor()  
    c.execute("SELECT rowid, * FROM customers")
    items = c.fetchall()
    for item in items:
        print(item)
    conn.commit()
    conn.close()
    
def add_one(first,last,email):
    conn = sqlite3.connect('customer.db')
    c = conn.cursor()  
    c.execute("INSERT INTO customers VALUES (?,?,?)", (first, last, email))
    conn.commit()
    conn.close()

def delete_one(id):
    conn = sqlite3.connect('customer.db')
    c = conn.cursor()  
    c.execute("DELETE from customers WHERE rowid = (?)", id)
    conn.commit()
    conn.close()

def add_many(list):
    conn = sqlite3.connect('customer.db')
    c = conn.cursor()  
    c.executemany("INSERT INTO customers VALUES (?,?,?)", (list))
    conn.commit()
    conn.close()
    
def email_lookup(email):
    conn = sqlite3.connect('customer.db')
    c = conn.cursor()  
    c.execute("SELECT rowid, * FROM customers WHERE email = (?)", (email,))
    items = c.fetchall()
    for item in items:
        print(item)
    conn.commit()
    conn.close()
    
# many_customers = [
#     ('John', 'Elder', 'john@codemy.com'),
#     ('Tim', 'Smith', 'tim@codemy.com'),
#     ('Mary', 'Brown', 'mary@codemy.com'),
#     ('Wes', 'Brown', 'wes@brown.com'),
#     ('Steph', 'Kuewa', 'steph@kuewa.com'),
#     ('Dan', 'Pasan', 'dan@pas.com')
# ]

# c.executemany("INSERT INTO customers VALUES (?,?,?)", many_customers)

# c.execute("Insert INTO customers VALUES ('Mary', 'Brown', 'mary@codemy.com')")
#Update Records

# c.execute ("""UPDATE customers SET email = 'john@codemy.com'
#             WHERE last_name = 'Elder'
#     """)
# conn.commit()

# c.execute ("""UPDATE customers SET last_name = 'Pasan'
#            WHERE rowid = 5
#      """)
# conn.commit()
# Query the Database
# c.execute("SELECT rowid, * FROM customers WHERE last_name LIKE 'Br%' AND rowid = 3")


#Delete Records
# c.execute("DELETE from customers WHERE rowid = 6")

#Query The Database - Order by
# c.execute("SELECT rowid, * FROM customers ORDER BY rowid DESC")
# c.execute("SELECT rowid, * FROM customers ORDER BY last_name DESC")

#Limits
# c.execute("SELECT rowid, * FROM customers ORDER BY rowid DESC LIMIT 3 ")

#Delete a Table Drop Table
# c.execute("DROP TABLE customers")

# c.execute("SELECT rowid, * FROM customers")

# print(c.fetchone())
# print(c.fetchmany(3))
# print(c.fetchall())
# items = c.fetchall()

# for item in items:
#     print(item)
# print("ID" + "\tNAME" + "\t\tEMAIL")
# print("--" + "\t-----" + "\t\t-----")
# for item in items:
#     print( str(item[0])  + "\t" + item[1] +  
#           " " + item[2] +
#           "\t" + item[3])

# print("Command executed successfully...")
# Commit our command
conn.commit()
# Close our connection
conn.close()