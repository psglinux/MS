import sys
import pymongo

class Customer:
    def __init__(self, name, email, phone, address):
        self.cname = name
        self.cemail = email
        self.cphone = phone
        self.caddress = address

    def name(self):
        return self.cname
    def name_is(self, cname):
        self.cname = cname

    def email(self):
        return self.cemail
    def email_is(self, cemail):
        #XXX TODO  Add validation
        self.cemail = email

    def phone(self):
        return self.cphone
    def phone_is(self, cphone):
        #XXX TODO  Add validation
        self.cphone = cphone

    def address(self):
        return self.caddress
    def address_is(self, caddress):
        self.caddress = caddress

    def fully_populated(self):
        if not self.cname:
            return False
        if not self.email:
            return False
        if not self.phone:
            return False
        if not self.address:
            return False
        return True

def add_customer(db, cust):
    # Verify that new customer has all information needed
    if not cust.fully_populated(): 
        return False

    # For purposes of unique customer identifcation, we will use email ID
    if db.customers.find_one({'email_address': cust.email()}):
       return False

    try:
        db.customers.insert_one({'Name': cust.name(), 'email_address': cust.email(),
                                'address': cust.address(), 'phone_number': cust.phone()})
    except:
        return False

    return True

'''
class CustomerOrder:
    def __init__(self, cust_id, cust_name, booksToQuantity={}, Cost):
        self.cust_id = cust_id
        self.cust_name = cust_name
        self.booksToQuantity = booksToQuantity
        self.Cost = self.calculate_cost()

    def calculate_cost():
        # Find books in booksToQuantity and cost of each to calculate total
        # cost to the customer
        return 0

def order_books(db, cust_id, booksToQuantity={}):
    # Find if all books requested exist ?
    # If, not then fail order.

    # Create a CustomerOrder Object to return to customer

    # Reduce books & quantity from inventory

    # Return Object
'''

