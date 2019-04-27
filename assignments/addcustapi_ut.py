import unittest
import mongomock
import json
import addcustapi

book1 = 'A test book'
book2 = 'Another test book'
book3 = 'A rare book'
cust_email = 'cl@gm.com'

class AddCustTests(unittest.TestCase):
    def setUp(self):
        self.db = mongomock.MongoClient()['testdb']

        cust = addcustapi.Customer('Clala', cust_email, '3131324411', '831001')
        ret = addcustapi.add_customer(self.db, cust)
        self.assertEqual(ret, True)
        # Setup for the second test
        self.db.books.insert_one({'_id': '1', 'Title': book1, 'Price': '1', 'ISBN-13':'djksdksdksd'})
        self.db.books.insert_one({'_id': '2', 'Title': book2, 'Price': '4', 'ISBN-13':'fdsffsdfs' })
        self.db.books.insert_one({'_id': '3', 'Title': book3, 'Price': '40', 'ISBN-13':'fsdjfsdjjsd'})
        self.db.inventory.insert_one({'_id': '1', 'quantity': 5})
        self.db.inventory.insert_one({'_id': '2', 'quantity': 3})
        self.db.inventory.insert_one({'_id': '3', 'quantity': 1})


    def tearDown(self):
        pass

    def test_add_customer(self):
        cust = addcustapi.Customer('Partha', 'psglinux@gm.com', '3131311111', '831002')
        ret = addcustapi.add_customer(self.db, cust)
        self.assertEqual(ret, True)

        # Re-use of email ID - not permitted
        cust = addcustapi.Customer('Pavan', cust_email, '3131311111', '831002')
        ret = addcustapi.add_customer(self.db, cust)
        self.assertEqual(ret, False)

        # Fixed email should work
        cust = addcustapi.Customer('Pavan', 'pavan@gm.com', '3131311111', '831002')
        ret = addcustapi.add_customer(self.db, cust)
        self.assertEqual(ret, True)

        num_cust = 0
        for customer in self.db.customers.find({}):
            num_cust += 1
        self.assertEqual(num_cust, 3)
        print("PASS add customer tests")

    def test_customer_order(self):
        # Send an order for a few books.
        book_to_qty = {book1 : 3, book2 : 4, book3 : 0} 
        customer, order = addcustapi.order_books(self.db, cust_email, book_to_qty)
        print(customer)
        self.assertEqual(customer['email_address'], cust_email) 
        self.assertEqual(customer['Name'], 'Clala') 
        print(order)
        self.assertEqual(len(order), 1)
        self.assertEqual(order[0]['Title'], book1)
        
if __name__ == '__main__':
    unittest.main()
