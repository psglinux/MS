import unittest
import mongomock
import json
import bookapi
import pprint

class DBTests(unittest.TestCase):
    def setUp(self):
        self.db = mongomock.MongoClient()['testdb']
        self.db.book.insert_one({'_id': '1', 'title': 'A test book'})
        self.db.book.insert_one({'_id': '2', 'title': 'Another test book'})
        self.db.book.insert_one({'_id': '3', 'title': 'A rare book'})
        self.db.inventory.insert_one({'_id': '1', 'id': '1', 'quantity': 5})
        self.db.inventory.insert_one({'_id': '2', 'id': '2', 'quantity': 0})
        self.db.inventory.insert_one({'_id': '3', 'id': '4', 'quantity': 1})

    def tearDown(self):
        pass

    def test_get_available_books(self):
        books = bookapi.get_available_books(self.db)
        self.assertEqual(len(books), 2)
        pprint.pprint(books)
        print("PASS bookapi test")

if __name__ == '__main__':
    unittest.main()
