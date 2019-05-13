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

class LoginAppTestCase(unittest.TestCase):
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

    def test_login_app(self):
        """
        Test the login app base url
        """
        tester = login.test_client(self)
        response = tester.get('/', content_type='html/text')
        print('login response:', response.get_data())
        pass

    def test_login(self):
        """
        Test the login api in the login app
        email_id,salt,sha256(salt+md5hash)
        email_id,salt,md5hash
        95f7vcnewd8@iffymedia.com,FF,5f4dcc3b5aa765d61d8327deb882cf99
        zo71ht9vbrp@payspun.com,AA,5f4dcc3b5aa765d61d8327deb882cf99
        6c2uj5sb352@fakemailgenerator.net,BB,5f4dcc3b5aa765d61d8327deb882cf99
        """
        data =   {'email_address': 'psg@gmail.com', 'password': 'md5hashed-password-from-ui'}
        pdata1 = {'email_address':'95f7vcnewd8@iffymedia.com', 'password':'5f4dcc3b5aa765d61d8327deb882cf99'}
        pdata_er1 = {'email_address':'95f7vcnewd8@iffymedia.com', 'password':'ccdfc3b5aa765d61d8327deb882cf99'}
        pdata2 = {'email_address':'zo71ht9vbrp@payspun.com','password':'5f4dcc3b5aa765d61d8327deb882cf99'}
        pdata3 = {'email_address':'6c2uj5sb352@fakemailgenerator.net', 'password':'5f4dcc3b5aa765d61d8327deb882cf99'}

        #test 1 match password
        tester = login.test_client(self)
        headers = {'content-type': 'application/json'}
        response = tester.post('/login', data=json.dumps(pdata1), headers=headers)
        #print('login response:', response.get_data())
        resp = json.loads(response.get_data())
        print("resp:", resp)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(resp['status'], 'success')
        print('login successfully tested')

        #test 2 try matching wrong password
        tester = login.test_client(self)
        headers = {'content-type': 'application/json'}
        response = tester.post('/login', data=json.dumps(pdata_er1), headers=headers)
        #print('login response:', response.get_data())
        resp = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(resp['status'], 'error')
        print('login password mismatch successfully tested')
        pass


if __name__ == '__main__':
    unittest.main()
