import unittest
import mongomock
import json
import addcustapi

class AddCustTests(unittest.TestCase):
    def setUp(self):
        self.db = mongomock.MongoClient()['testdb']

        self.db.book.insert_one({'_id': '1', 'title': 'A test book', 'cost': '1'})
        self.db.book.insert_one({'_id': '2', 'title': 'Another test book', 'cost': '4' })
        self.db.book.insert_one({'_id': '3', 'title': 'A rare book', 'cost': '40'})
        self.db.inventory.insert_one({'_id': '1', 'id': '1', 'quantity': 5})
        self.db.inventory.insert_one({'_id': '2', 'id': '2', 'quantity': 3})
        self.db.inventory.insert_one({'_id': '3', 'id': '4', 'quantity': 1})

        cust = addcustapi.Customer('Clala', 'cl@gm.com', '3131324411', '831001')
        ret = addcustapi.add_customer(self.db, cust)
        self.assertEqual(ret, True)

    def tearDown(self):
        pass

    def test_add_customer(self):
        cust = addcustapi.Customer('Partha', 'psglinux@gm.com', '3131311111', '831002')
        ret = addcustapi.add_customer(self.db, cust)
        self.assertEqual(ret, True)

        # Re-use of email ID - not permitted
        cust = addcustapi.Customer('Pavan', 'cl@gm.com', '3131311111', '831002')
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
        print("PASS AddCustTests")

if __name__ == '__main__':
    unittest.main()
