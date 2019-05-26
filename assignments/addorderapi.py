import random
from datetime import datetime
from bson import ObjectId

class Order:
    def __init__(self, order_dict):
        self.order_id = ""
        self.order_dict=order_dict
        self.created_time = str(datetime.utcnow())
        self.completed_time = ""
        self.status = "Initiated"

    def name_is(self, email):
        self.email = email

    def created_time(self):
        return self.created_time

    def created_time_is(self, created_time):
        self.created_time = created_time

    def status(self):
        return self.status

    def status_is(self, status):
        self.status = status

    def fully_populated(self):
        if not self.status:
            return False
        return True

def get_all_order(db):
    """
    get all the oders from the db and return a json
    """
    try:
        orders  = db.orders.find()
        print(orders)
    except Exception as e:
        print("get order exception", str(e))

def create_order(db, order):
    # Verify that new order has all information needed
    dict_order_info = {}
    if not order.fully_populated():
        dict_order_info = {"error":"order info not fully populated"}
        return dict_order_info
    try:
        print(order.order_dict)
        #### check if the customer exist ####
        customer = db.customers.find_one({'email_address': order.order_dict["email"]})
        print(customer)
        if customer is None:
            dict_order_info = {"error": "customer does not exist"}
            return dict_order_info

        #### check if the book id exist ####
        for ordered_book in order.order_dict["order"]:
            book_id=ordered_book["book_id"]
            print(book_id)
            book = db.book.find_one({'_id': ObjectId(book_id)})

        if book is None:
            dict_order_info = {"error": "book does not exist"}
            return dict_order_info
        ##### create random number for order_id ######
        ### TODO : Need to check how to make it unique

        order_no = random.randint(256,4567890098765456789)
        order.order_id = order_no
        db.orders.insert_one({'order_id': order.order_id,"order_dtl":order.order_dict, 'created_time': order.created_time, 'status': order.status})

        ####check if order inserted properly and return the order number####

        order = db.orders.find_one({'order_id': order.order_id})
        if order is not None:
            dict_order_info = {"order_id": order["order_id"]}
            return dict_order_info
        else:
            dict_order_info = {"error": "order id is not created successfully due to some technical issue"}
            return dict_order_info
    except Exception as e:
        print("exception:" + str(e))
    return dict_order_info

# Customer will order books based on the following
# - Will provide customer email
# - Will provide provide book names and quantities
# Verify this customer exists in Customer DB else fail order
#
# The API will look up books collection to find via book name
# - id of each book
# - Price of each book
#
# After this API will use id to query inventory collection
# - Check if requested quantity for each book is available
# - Decrement in book inventory if everything is available else fail order
#
# Open Items: How to charge customer ? We don't have payment info in the
# Customer table.
#
# XXX TODO Note: Some of this will change when we add AUTH because we need to
# pull user information from an authenticated session object which
# identifies an authenticated user.
def process_order(db, order_id):
    books_order = []
    order_val = db.orders.find_one({'order_id': int(order_id)})
    print("order_val:",order_val)
    if not order_val:
        return "ERROR"

    db.orders.update_one({'order_id': int(order_id)}, {'$set': {'status': 'in_processing'}}, upsert=False)
    for book_order in order_val["order_dtl"]["order"]:
            print(book_order)
            book_record = db.book.find_one({'_id': ObjectId(book_order["book_id"])})
            print(book_record)
            book_id = book_record['_id']
            book_inventory = None
            try:
                book_inventory = db.inventory.find_one({'_id': book_id})
            except:
                continue

            inv_qty = int(book_inventory['quantity'])
            req_qty = int(book_order["quantity"])
            if req_qty <= 0 or inv_qty < req_qty:
                db.orders.update_one({'order_id': order_id},
                                 {'$set': {'status': 'pending'}}, upsert=False)
            else:
                remain_qty = inv_qty - req_qty
            try:
                db.inventory.update_one({'_id': book_id}, {'$set': {'quantity': remain_qty}}, upsert=False)
                db.orders.update_one({'order_id': order_id},
                                     {'$set': {'status': 'completed', 'completed_time': str(datetime.utcnow())}}, upsert=False)
            except:
                continue
    books_order.append(order_id)
    return str(books_order)
