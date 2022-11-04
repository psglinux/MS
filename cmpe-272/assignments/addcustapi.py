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
        self.cemail = cemail

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
def order_books(db, cust_email, book_to_qty={}):
    customer = db.customers.find_one({'email_address': cust_email})
    if not customer:
        return None

    books_order = []
    for title, req_qty in book_to_qty.items():
        book_record = None
        try:
            book_record = db.books.find_one({'Title': title})
        except:
            continue
        book_id = book_record['_id']
        book_inventory = None
        try:
            book_inventory = db.inventory.find_one({'_id': book_id})
        except:
            continue

        # XXX TODO HACK ALERT! Do we really know that this remain_qty will be atomically set ?
        # What is the syntax for "Atomically read and decrement this amount" from DB ?
        inv_qty = book_inventory['quantity']
        if req_qty <= 0 or inv_qty < req_qty:
            continue
        remain_qty = inv_qty - req_qty
        try:
            db.inventory.update_one({'_id': book_id}, {'$set': {'quantity': remain_qty}}, upsert=False)
        except:
            continue
        book_order = {'Title':title, 'ISBN-13': book_record['ISBN-13'], 'Price':book_record['Price'], 'Quantity':req_qty}
        books_order.append(book_order)

    # This will be a set of customer object & a list of books
    # Each book is a dict of book title, ISBN-13, price and qty
    return (customer, books_order)

