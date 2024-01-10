import database

#add a record to the database
# database.add_one('Laura', 'Smith', 'laura@smith.com')

#Delete record with rowid = 6 as a string
# database.delete_one('7')

#Add Many Records

# stuff = [
#     ('Brenda', 'Smitherton', 'brenda@smitherton.com'),
#     ('Joshua', 'Raintree', 'josh@raintree.com')
# ]
# database.add_many(stuff)

database.email_lookup('john@codemy.com')

# database.show_all()