import unittest
import mongomock
import json
import addcustapi

class AddCustTests(unittest.TestCase):
    def setUp(self):
        self.db = mongomock.MongoClient()['testdb']
        self.db.customers.insert_one({'_id': '1000', 'name': 'Clala'})

    def tearDown(self):
        pass

    def test_add_customer(self):
        ret = addcustapi.add_customer(self.db, cust_id='100', cust_name='Partha')
        self.assertEqual(ret, True)
        ret = addcustapi.add_customer(self.db, cust_id='1000', cust_name='Pavan')
        self.assertEqual(ret, False)
        ret = addcustapi.add_customer(self.db, cust_id='2', cust_name='Kani')
        self.assertEqual(ret, True)

        num_cust = 0
        for customer in self.db.customers.find({}):
            num_cust += 1
        self.assertEqual(num_cust, 3)
        print("PASS AddCustTests")

if __name__ == '__main__':
    unittest.main()
