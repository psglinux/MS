import unittest
import mongomock
import json
import bookapi
import pprint
from apymongodb import APymongodb

class DBTests(unittest.TestCase):
    def setUp(self):
        self.pymondb = APymongodb(test=True)
        self.pymondb.create_db_from_csv()

    def tearDown(self):
        pass

    def test_get_available_books(self):
        books = bookapi.get_available_books(self.pymondb.db)
        #print("len", len(books))
        self.assertEqual(len(books), 10)
        pprint.pprint(books)
        print("PASS bookapi test")

if __name__ == '__main__':
    unittest.main()
