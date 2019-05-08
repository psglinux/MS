import unittest
import os
import json
import mongomock
import bookapi
import pprint

from app import app
from login import login
import apymongodb

TEST_DB = 'test_database'


class BasicTestCase(unittest.TestCase):

    def setUp(self):
        """
        Set up a temp database before each test. since this is not end to
        end test use mongomock to create a testdb. This DB will have the same
        schema as that of the original db.
        """
        app.testing = True
        pass

    def tearDown(self):
        """using mongomock for the ut test. Hence no clean up is needed """
        pass

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
        print("response :", dir(response))
        print("response.mime_type :", response.mimetype)
        print("response.mime_type_params :", response.mimetype_params)
        print("response.json:", response.json)
        print("get all books:", response.get_data())
        #print("get all books:", response)
        self.assertEqual(response.status_code, 200)
        pass

    def test_get_book_isbn(self):
        """
        Test the book isbn api
        """
        tester = app.test_client(self)
        response = tester.get('/getbook/123', content_type='html/text')
        print(response.get_data())
        self.assertEqual(response.status_code, 200)

        tester = app.test_client(self)
        response = tester.get('/getbook/1491979909', content_type='html/text')
        print(response.get_data())
        self.assertEqual(response.status_code, 200)

        tester = app.test_client(self)
        response = tester.get('/getbook/978-0201616224', content_type='html/text')
        #print("dir response:", dir(response))
        #print("type",type(response.get_data()))
        print("data: ",(response.get_data()))
        #print(response.get_json())
        self.assertEqual(response.status_code, 200)
        pass

    def test_process_book_order(self):
        """
        Test the books api
        """
        tester = app.test_client(self)
        response = tester.put('/processorder/4321312', content_type='html/text')
        print("process order:", response.get_data())
        #print("get all books:", response)
        self.assertEqual(response.status_code, 404)
        pass

    def test_login_process(self):
        """
        Test the login api from the main app
        """
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        print('login response:', response.get_data())
        pass

    def test_login_app(self):
        """
        Test the login api in teh login app
        """
        tester = login.test_client(self)
        response = tester.get('/', content_type='html/text')
        print('login response:', response.get_data())
        pass


if __name__ == '__main__':
    unittest.main()
