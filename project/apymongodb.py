import sys
import pymongo
import mongomock
import json
import csv
from pymongo import MongoClient
import sys
import hashlib
from pprint import pprint


class APymongodb:
    def __init__(self, uri="project-mongodb", db_name="client_database", test=False):
        if test:
            self.db =mongomock.MongoClient()[db_name]
        else:
            self.db = pymongo.MongoClient(uri)[db_name]
        pass

    def delete_db(self):
        pass

    def populate_db_json(self, collection, jfile):
        """
        read json from a file and populate the db
        """
        pass

    def test_read_project_db(self):
        """
        read all element from the project db
        """
        cal = self.db.calendar.find({})
        print("type cal:", type(cal), dir(cal))
        print("cal count:", cal.count())
        lst = self.db.listings.find({})
        print("type lst:", type(lst), dir(lst))
        print("lst count:", lst.count())
        rev = self.db.reviews.find({})
        print("type rev:", type(rev), dir(rev))
        print("rev count:", rev.count())
        pass

    def create_project_db_from_csv(self):
        cal_coll = self.db.calender
        list_coll = self.db.listings
        rev_coll = self.db.reviews
        with open('testdb/calendar.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                #print("type",type(row), "data", row)
                cal_coll.insert_one(dict(row))
        with open('testdb/listings.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                #print("type",type(row), "data", row)
                list_coll.insert_one(dict(row))
        with open('testdb/reviews.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                #print("type",type(row), "data", row)
                rev_coll.insert_one(dict(row))
        pass

    def create_auth_db(self):
        ## creating authentication collection for login_id,salt,password collections
        self.db.authentication.drop()
        login_collection = self.db.authentication
        #login.csv contains the password in md5hash
        with open('testdb/login.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                #print("type",type(row), "data", row)
                #print('email_address:', row['email_address'], 'salt:', row['salt'], 'password:', row['password'])
                #print(hashlib.sha256(str(row['salt']+hashlib.md5('password'.encode('utf-8')).hexdigest()).encode('utf-8')).hexdigest())
                row['password'] = hashlib.sha256(str(row['salt']+hashlib.md5('password'.encode('utf-8')).hexdigest()).encode('utf-8')).hexdigest()
                login_collection.insert_one(dict(row))

if __name__ == '__main__':
    argv = sys.argv
    if len(argv) < 2:
        print("Usage: python3 " + argv[0] + " mongodb_uri")
        exit(-1)

    mongodb_uri = argv[1]
    #pymondb = APymongodb(test=True)
    pymondb = APymongodb(mongodb_uri, "client_database", False)
    pymondb.create_project_db_from_csv()
    #pymondb.test_read_project_db()
    pymondb.create_auth_db()

