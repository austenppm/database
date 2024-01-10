import assignment4 as a4
import sqlite3
from faker import Faker 
from pydbgen import pydbgen
import pandas as pd 
import random
import datetime
from collections import defaultdict
from sqlalchemy import create_engine

fake = Faker()
ourDB = pydbgen.pydb()

a4.init_db()

# def make_profile_User(x, y):
#     Faker.seed(x)
#     profiles_Users = pd.DataFrame([{
#         'UserID': i + 1,  # Generating a simple UserID based on the loop index
#         'Username': profile['username'],
#         'Password': fake.password(),  # Generate a random password using Faker
#         'Email': profile['mail'],
#         'PhoneNumber': fake.msisdn(),  # Use Faker to generate a phone number
#         'FlagStatus': 'Normal' if random.random() < 0.95 else 'Flagged For Review',  # Example: alternating Normal and Flagged status
#     } for i, profile in enumerate([fake.simple_profile() for _ in range(y)])])
#     profiles_Users['created'] = datetime.datetime.now()
#     return profiles_Users



# # Assuming you want to insert the generated data into the User table
# def insert_users_to_db_User(df):
#     conn = sqlite3.connect('restaurant_management.db')
#     c = conn.cursor()
    
#     # Deduplicate profiles based on Email
#     df = df.drop_duplicates(subset='Email', keep='first')
    
#     for index, row in df.iterrows():
#         c.execute("INSERT OR IGNORE INTO User (UserID, Username, Password, Email, PhoneNumber, FlagStatus) VALUES (?, ?, ?, ?, ?, ?)", 
#             (row['UserID'], row['Username'], row['Password'], row['Email'], row['PhoneNumber'], row['FlagStatus']))
#     conn.commit()
#     conn.close()

# def make_profile_Admin(x, y):
#     Faker.seed(x)
#     profiles_Users = pd.DataFrame([{
#         'UserID': i + 1,  # Generating a simple UserID based on the loop index
#         'Username': profile['username'],
#         'Password': fake.password(),  # Generate a random password using Faker
#         'Email': profile['mail'],
#         'PhoneNumber': fake.msisdn(),  # Use Faker to generate a phone number
#         'FlagStatus': 'Normal' if random.random() < 0.95 else 'Flagged For Review',  # Example: alternating Normal and Flagged status
#     } for i, profile in enumerate([fake.simple_profile() for _ in range(y)])])
#     profiles_Users['created'] = datetime.datetime.now()
#     return profiles_Users



# # Assuming you want to insert the generated data into the User table
# def insert_users_to_db_Admin(df):
#     conn = sqlite3.connect('restaurant_management.db')
#     c = conn.cursor()
    
#     # Deduplicate profiles based on Email
#     df = df.drop_duplicates(subset='Email', keep='first')
    
#     for index, row in df.iterrows():
#         c.execute("INSERT OR IGNORE INTO User (UserID, Username, Password, Email, PhoneNumber, FlagStatus) VALUES (?, ?, ?, ?, ?, ?)", 
#             (row['UserID'], row['Username'], row['Password'], row['Email'], row['PhoneNumber'], row['FlagStatus']))
#     conn.commit()
#     conn.close()

def get_random_ids(num, id_list):
    return random.sample(id_list, num)

# Function to generate users
def make_unique_users(num_users):
    users = []
    generated_emails = set()  # Set to keep track of emails already generated

    while len(users) < num_users:
        email = fake.email()
        if email not in generated_emails:
            generated_emails.add(email)
            users.append({
                'Username': fake.user_name(),
                'Password': fake.password(),
                'Email': email,
                'PhoneNumber': fake.msisdn(),
                'FlagStatus': 'Normal' if random.random() < 0.95 else 'Flagged For Review',
            })
    return users

# Function to insert users and return user IDs with 'User' prefix
def insert_unique_users(users):
    conn = sqlite3.connect('restaurant_management.db')
    c = conn.cursor()
    user_ids = []

    for user in users:
        # Check if the email already exists in the User table
        c.execute("SELECT Email FROM User WHERE Email = ?", (user['Email'],))
        if c.fetchone() is None:  # If email does not exist, insert the new user
            c.execute("""
                INSERT INTO User (Username, Password, Email, PhoneNumber, FlagStatus) 
                VALUES (?, ?, ?, ?, ?)
                """, (user['Username'], user['Password'], user['Email'], user['PhoneNumber'], user['FlagStatus']))
            # Get the last inserted ID, add prefix, and append to the list
            new_id = c.lastrowid
            # Generate the prefixed UserID
            prefixed_user_id = f"USER_{str(new_id).zfill(8)}"  # Pad the ID with zeros

            # Update the UserID with the new prefixed ID
            c.execute("UPDATE User SET UserID = ? WHERE rowid = ?", (prefixed_user_id, new_id))
            user_ids.append(prefixed_user_id)
        else:
            print(f"Duplicate email found: {user['Email']} - User not inserted.")

    conn.commit()
    conn.close()
    return user_ids

def get_random_ids(num, user_ids):
    # Ensure this function returns unique IDs
    return random.sample(user_ids, num)

def insert_admins(num_admins, user_ids):
    conn = sqlite3.connect('restaurant_management.db')
    c = conn.cursor()
    inserted_admin_ids = []

    while len(inserted_admin_ids) < num_admins:
        # Select a random user ID from the list
        admin_user_id = random.choice(user_ids)
        # Check if this user ID is already assigned to an admin
        c.execute("SELECT UserID FROM Admin WHERE UserID = ?", (admin_user_id,))
        if c.fetchone() is None:
            system_settings_access = random.choices(['Full Access', 'Limited Access', 'No Access'], weights=[2, 5, 3], k=1)[0]
            system_monitoring_access = random.choices(['Full Access', 'Limited Access'], weights=[7, 3], k=1)[0]
            c.execute("""
                INSERT INTO Admin (SystemSettings, SystemMonitoring, UserID) 
                VALUES (?, ?, ?)
                """, (system_settings_access, system_monitoring_access, admin_user_id))
            new_admin_id = c.lastrowid
            
            # Generate the prefixed AdminID
            prefixed_admin_id = f"ADMIN_{str(new_admin_id).zfill(8)}"
            # Update the AdminID with the new prefixed ID
            c.execute("UPDATE Admin SET AdminID = ? WHERE rowid = ?", (prefixed_admin_id, new_admin_id))
            
            # Append the prefixed AdminID to the list
            inserted_admin_ids.append(prefixed_admin_id)
            # Remove the used UserID from the list to avoid re-selection
            user_ids.remove(admin_user_id)
        else:
            # If the user ID is already an admin, remove it from the list and try another one
            user_ids.remove(admin_user_id)
            
    conn.commit()
    conn.close()
    
    return inserted_admin_ids


# Function to insert customers
def insert_customers(num_customers, user_ids):
    conn = sqlite3.connect('restaurant_management.db')
    c = conn.cursor()
    customer_ids = get_random_ids(num_customers, user_ids)

    if not customer_ids:
        print("No customer IDs provided for insertion.")
        return []

    inserted_customer_ids = []

    for user_id in customer_ids:
        try:
            # Fetch the username for the user ID
            c.execute("SELECT Username FROM User WHERE UserID = ?", (user_id,))
            result = c.fetchone()
            if result:
                username = result[0]

                # Generate a prefixed CustomerID
                c.execute("SELECT COUNT(*) FROM Customer")
                count = c.fetchone()[0]
                prefixed_customer_id = f"CUS_{str(count + 1).zfill(7)}"

                # Check if the customer ID already exists in the Customer table
                c.execute("SELECT CustomerID FROM Customer WHERE UserID = ?", (user_id,))
                if c.fetchone() is None:
                    allergies = random.choices(['None', 'One', 'Several'], weights=[6, 2, 2], k=1)[0]
                    c.execute("""
                        INSERT INTO Customer (CustomerID, UserID, Username, LoyaltyPoints, Age, Gender, Allergies) 
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        """, (prefixed_customer_id, user_id, username, random.randint(0, 5000), random.randint(18, 100), random.choice(['Male', 'Female', 'Other']), allergies))
                    inserted_customer_ids.append(prefixed_customer_id)
                else:
                    print(f"User ID {user_id} already has a customer profile - Customer not inserted.")
            else:
                print(f"No username found for User ID {user_id} - Customer not inserted.")
        except sqlite3.IntegrityError as e:
            print(f"IntegrityError: {e}")
        except sqlite3.OperationalError as e:
            print(f"OperationalError: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    conn.commit()
    conn.close()
    return inserted_customer_ids



# Function to insert restaurants and return restaurant IDs
def insert_restaurants(restaurant_ids):
    conn = sqlite3.connect('restaurant_management.db')
    c = conn.cursor()
    inserted_restaurant_ids = []

    for user_id in restaurant_ids:
        # Fetch the username for the user ID
        c.execute("SELECT Username FROM User WHERE UserID = ?", (user_id,))
        result = c.fetchone()
        if result:
            username = result[0]

            # Generate a unique RestaurantID
            c.execute("SELECT COUNT(*) FROM Restaurant")
            count = c.fetchone()[0]
            prefixed_restaurant_id = f"RES_{str(count + 1).zfill(7)}"

            # Generate other restaurant details
            price_range = [1000 * i for i in range(1, 11)] + [10000 + 5000 * i for i in range(1, 9)]
            price_label = random.choice(price_range)
            price = f"{price_label}+" if price_label >= 10000 else f"{price_label - 1000} ~ {price_label}"

            # Insert the restaurant
            c.execute("""
                INSERT INTO Restaurant (RestaurantID, UserID, Username, RestaurantName, RestaurantDescription, CuisineType, Price, Location) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (prefixed_restaurant_id, user_id, username, fake.company(), fake.text(max_nb_chars=100), fake.word(), price, fake.address()))

            inserted_restaurant_ids.append(prefixed_restaurant_id)
        else:
            print(f"No username found for User ID {user_id} - Restaurant not inserted.")

    conn.commit()
    conn.close()
    return inserted_restaurant_ids

#Function to insert reviews
def insert_reviews(num_reviews, customer_ids, restaurant_ids, reservation_ids):
    conn = sqlite3.connect('restaurant_management.db')
    c = conn.cursor()

    # Get the current count of reviews for prefixing
    c.execute("SELECT COUNT(*) FROM Review")
    count = c.fetchone()[0]

    reviewed_reservations = set()

    for _ in range(num_reviews):
        # Generate a prefixed ReviewID
        prefixed_review_id = f"REV_{str(count + 1).zfill(6)}"
        count += 1

        has_reservation = random.random() < 0.6  # 60% chance to have a reservation
        if has_reservation and reservation_ids:
            reservation_id = random.choice(reservation_ids)
            if reservation_id in reviewed_reservations:
                # Skip this reservation as it already has a review
                continue
            reviewed_reservations.add(reservation_id)

            # Fetch the customer and restaurant IDs from the reservation
            c.execute("SELECT CustomerID, RestaurantID FROM Reservation WHERE ReservationID = ?", (reservation_id,))
            result = c.fetchone()
            if result:
                customer_id, restaurant_id = result
                verified = "Verified" if random.random() < 0.9 else "Unverified"  # 90% chance of being verified
            else:
                continue  # Skip if the reservation is not found
        else:
            reservation_id = "NIL"
            customer_id = random.choice(customer_ids)
            restaurant_id = random.choice(restaurant_ids)
            verified = "Unverified"

        rating = random.choices([1, 2, 3, 4, 5], weights=[1, 1, 2, 5, 3], k=1)[0]

        c.execute("""
            INSERT INTO Review (ReviewID, CustomerID, RestaurantID, ReservationID, VerificationStatus, Rating, Comments) 
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (prefixed_review_id, customer_id, restaurant_id, reservation_id, verified, rating, fake.text(max_nb_chars=200)))

    conn.commit()
    conn.close()


# Function to insert reservations and return reservation IDs
def insert_reservations(num_reservations, customer_ids, restaurant_ids):
    conn = sqlite3.connect('restaurant_management.db')
    c = conn.cursor()
    
    # Get the current count of reservations
    c.execute("SELECT COUNT(*) FROM Reservation")
    count = c.fetchone()[0]
    
    reservation_ids = []
    
    for i in range(num_reservations):
            # Generating a prefixed ReservationID
            prefixed_reservation_id = f"RSV_{str(count + 1).zfill(5)}"
            count += 1  # Increment for the next ID

            # Weighted number of people, most common from 1 to 15
            num_people = random.choices(range(1, 101), weights=[5]*15 + [1]*85, k=1)[0]

            # Weighted choice for reservation status
            status = random.choices(['Confirmed', 'Cancelled', 'Pending'], weights=[70, 20, 10], k=1)[0]

            c.execute("""
                INSERT INTO Reservation (ReservationID, CustomerID, RestaurantID, NumberOfPeople, Time, Allergies, Notes, PaymentInfo, Status) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (prefixed_reservation_id, random.choice(customer_ids), random.choice(restaurant_ids), num_people, fake.date_time_this_year(), fake.sentence(), fake.sentence(), fake.credit_card_number(), status))
            
            # Append the new reservation_id to the list
            reservation_ids.append(prefixed_reservation_id)

    conn.commit()
    conn.close()
    return reservation_ids


def insert_system_data(access_rules):
    conn = sqlite3.connect('restaurant_management.db')
    c = conn.cursor()

    for rule in access_rules:
        # Unpacking the dictionary values
        system_data_id = rule['SystemDataID']
        data_type = rule['DataType']
        system_settings = rule['SystemSettings']
        system_monitoring = rule['SystemMonitoring']

        # Inserting each record
        c.execute("""
            INSERT INTO SystemData (SystemDataID, DataType, SystemSettings, SystemMonitoring) 
            VALUES (?, ?, ?, ?)
            """, (system_data_id, data_type, system_settings, system_monitoring))

    conn.commit()
    conn.close()

# Function to insert analytics
def insert_analytics(restaurant_ids):
    conn = sqlite3.connect('restaurant_management.db')
    c = conn.cursor()

    # Get the current count of analytics records for prefixing
    c.execute("SELECT COUNT(*) FROM Analytics")
    count = c.fetchone()[0]

    for restaurant_id in restaurant_ids:
        # Generate a prefixed AnalyticsID
        prefixed_analytics_id = f"ANA_{str(count + 1).zfill(6)}"
        count += 1

        # Calculate and round the average rating for the restaurant
        c.execute("SELECT AVG(Rating) FROM Review WHERE RestaurantID = ?", (restaurant_id,))
        avg_rating_result = c.fetchone()
        avg_rating = round(avg_rating_result[0], 2) if avg_rating_result[0] is not None else 0

        c.execute("""
            INSERT INTO Analytics (AnalyticsID, RestaurantID, MonthlyTraffic, AverageRating, PeakTimes) 
            VALUES (?, ?, ?, ?, ?)
            """, (prefixed_analytics_id, restaurant_id, random.randint(0, 10000), avg_rating, fake.time()))

    conn.commit()
    conn.close()


# Main execution
def main():
    num_users = 1000
    num_admins = 100
    num_customers = 800
    num_restaurants = 50
    num_reservations = 500
    num_reviews = 1000

    # Generate and insert users
    users = make_unique_users(num_users)
    user_ids = insert_unique_users(users)
    
    # Ensure user_ids is not empty before proceeding
    if not user_ids:
        print("No users were created. Exiting the program.")
        return

    # Insert admins using some of the user_ids
    admin_ids = insert_admins(num_admins, user_ids)
    
    # Randomly select customer_ids from the user_ids
    customer_ids = insert_customers(num_customers, user_ids)
    
    # Ensure customer_ids is not empty before proceeding
    if not customer_ids:
        print("Not enough users to create customers. Exiting the program.")
        return
    # The remaining user_ids that are not admins or customers will be used for restaurants
    remaining_user_ids = list(set(user_ids) - set(admin_ids) - set(customer_ids))
    
    # If there aren't enough remaining user_ids for the restaurants, handle the case appropriately
    if len(remaining_user_ids) < num_restaurants:
        print(f"Not enough unique users to assign as restaurants. Required: {num_restaurants}, Available: {len(remaining_user_ids)}")
        # Optionally, you could reduce num_restaurants or handle it differently
        return
    
    # Use the remaining user_ids as restaurant_ids
    to_insert_restaurant_ids = remaining_user_ids[:num_restaurants]    
    
    # Generate and insert restaurants
    restaurant_ids = insert_restaurants(to_insert_restaurant_ids)
    
    # Ensure restaurant_ids is not empty before proceeding
    if not restaurant_ids:
        print("No restaurants were created. Exiting the program.")
        return
    
    # Insert reservations now that we have valid customer and restaurant IDs
    reservation_ids = insert_reservations(num_reservations, customer_ids, restaurant_ids)
    
    #Insert reviews
    insert_reviews(num_reviews, customer_ids, restaurant_ids, reservation_ids)
    
    access_rules = [
        {"SystemDataID" : "SYS_0001", "DataType": "UserData", "SystemSettings": "Full Access", "SystemMonitoring": "Inapplicable"},
        {"SystemDataID" : "SYS_0002", "DataType": "Reservation", "SystemSettings": "Limited Access", "SystemMonitoring": "Inapplicable"},
        {"SystemDataID" : "SYS_0003", "DataType": "LoyaltyPoints", "SystemSettings": "Limited Access", "SystemMonitoring": "Inapplicable"},
        {"SystemDataID" : "SYS_0004", "DataType": "FlagStatus", "SystemSettings": "Inapplicable", "SystemMonitoring": "Limited Access"},
        {"SystemDataID" : "SYS_0005", "DataType": "Review", "SystemSettings": "Inapplicable", "SystemMonitoring": "Full Access"},
        {"SystemDataID" : "SYS_0006", "DataType": "Analytics", "SystemSettings": "Inapplicable", "SystemMonitoring": "Full Access"}
    ]
    # Now insert system data associated with these admins
    insert_system_data(access_rules)

# Defining the access rules based on the SystemSettings and SystemMonitoring access levels
    
    # Insert analytics for the restaurants
    insert_analytics(restaurant_ids)

if __name__ == "__main__":
    main()

# profiles_User = make_profile_User(1989, 1000)
# insert_users_to_db_User(profiles_User)

# table = input("Enter the table name: ")
# limit = input("Enter the limit: ")
# ascend_or_descend = input("Enter the order: ")

# a4.show_limit(table, ascend_or_descend, limit)
# a4.delete_table(table)
# a4.delete_alltablesandrelations()
a4.show_all_first_x(5)