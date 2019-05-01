import unittest
import os
import json

from app import app

TEST_DB = 'test_database'


class BasicTestCase(unittest.TestCase):

    def test_index(self):
        """initial test. ensure flask was set up correctly"""
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_get_book(self):
        """
        Test the books api
        """
        tester = app.test_client(self)
        response = tester.get('/getbook', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        pass

    def test_get_book_isbn(self):
        """
        Test the book isbn api
        """
        tester = app.test_client(self)
        response = tester.get('/getbook/123', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        pass

    def test_database(self):
        """initial test. ensure that the database exists"""
        pass


if __name__ == '__main__':
    unittest.main()
