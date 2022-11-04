import unittest
import mongomock
import json
import addcustapi
import addorderapi

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
        self.db.book.insert_one({'_id': '5ccf19759722a0ae42c6974b', 'title': book1, 'Price': '1', 'ISBN-13': 'djksdksdksd'})
        self.db.book.insert_one({'_id': '2', 'title': book2, 'Price': '4', 'ISBN-13': 'fdsffsdfs'})
        self.db.book.insert_one({'_id': '3', 'title': book3, 'Price': '40', 'ISBN-13': 'fsdjfsdjjsd'})
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

    def test_create_order(self):
        order = addorderapi.Order('psglinux@gm.com', book1, 3)
        dict_order_info = addorderapi.create_order(self.db, order)
        self.assertEqual(dict_order_info["error"], "customer does not exist")

        order = addorderapi.Order(cust_email, 'nobook', 4)
        dict_order_info = addorderapi.create_order(self.db, order)
        self.assertEqual(dict_order_info["error"], "book does not exist")

        order = addorderapi.Order(cust_email, book1, 4)
        dict_order_info = addorderapi.create_order(self.db, order)
        order = self.db.orders.find_one({'email': cust_email})
        self.assertEqual(str(dict_order_info["order_id"]), str(order["order_id"]))

        num_order = 0
        for order in self.db.orders.find({}):
            num_order += 1
        self.assertEqual(num_order, 1)
        print("PASS create order")

    def test_process_order(self):
        order_list =[]

        order1 = addorderapi.Order(cust_email, book1, 4)
        dict_order_info_1 = addorderapi.create_order(self.db, order1)
        order_find_1 = self.db.orders.find_one({'email': cust_email})
        self.assertEqual(str(dict_order_info_1["order_id"]), str(order_find_1["order_id"]))
        order_1 = order_find_1["order_id"]
        customer, orders = addorderapi.process_order(self.db, order_list)
        self.assertEqual(len(orders), 1)
        order_1 = self.db.orders.find_one({'order_id': order_1})
        print(order_1)
        self.assertEqual(order_1['status'], 'completed')

if __name__ == '__main__':
    unittest.main()
