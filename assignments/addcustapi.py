import sys
import pymongo

def add_customer(db, cust_id, cust_name):
    # Add new customer to pre-existing DB collection
    # Make sure the customer Id is unique. Then add
    # the given ID and Name to the collection
    if db.customers.find_one({'_id': cust_id}):
       return False

    try:
        db.customers.insert_one({'_id': cust_id, 'name': cust_name})
    except:
        return False

    return True

