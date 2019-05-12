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
    def __init__(self, uri="mongodb", db_name="test_database", test=False):
        if test:
            self.db =mongomock.MongoClient()[db_name]
        else:
            self.db = pymongo.MongoClient(uri)[dbname]
        pass

    def delete_db(self):
        pass

    def create_db_from_csv(self):
        """
        populate db from a csv file
        the top row of the csv file would indicate the key of the entry
        """
        # Find the unique authors and publishers
        author_list = []
        publisher_list = []
        with open("database/book.csv", newline='') as csvfile:
            bookreader = csv.DictReader(csvfile, delimiter=',')
            for row in bookreader:
                author_list_tmp = row['Author'].split(";")
                for author in author_list_tmp:
                    if author.strip() not in author_list:
                        author_list.append(author.strip())
                publisher = row['publisher'].strip()
                if publisher not in publisher_list:
                    publisher_list.append(publisher)
        # print(author_list)
        # print(publisher_list)

        # creating author collection and create documents
        self.db.author.drop()
        author_collection = self.db.author
        self.db.publisher.drop()
        publisher_collection = self.db.publisher

        for author_name in author_list:
            #print(author_name)
            author_dict = {"author": author_name}
            author_collection.insert_one(author_dict)
        cursor = author_collection.find({})
        for document in cursor:
            #pprint(document)
            pass
        for publisher_name in publisher_list:
            #print(publisher_name)
            publisher_dict = {"publisher": publisher_name}
            publisher_collection.insert_one(publisher_dict)
        cursor = publisher_collection.find({})
        for document in cursor:
            #pprint(document)
            pass
        print(self.db.list_collection_names())

        self.db.book.drop()
        book_collection = self.db.book
        self.db.inventory.drop()
        inventory_collection = self.db.inventory
        with open("database/book.csv", newline='') as csvfile:
            bookreader = csv.DictReader(csvfile, delimiter=',')

            for row in bookreader:
                dict1 = {}
                dict2 = {}
                #print(row)
                dict1["title"] = row["Title"]
                dict1["ISBN-13"] = row["ISBN-13"]
                dict1["ISBN-10"] = row["ISBN-10"]
                dict1["review_count"] = row["Reviews"]
                dict1["description"] = row["Book Description"]
                dict1["published"] = row["published"]
                dict1["pages"] = row["pages"]
                dict1["price"] = row["price"]
                author_list_tmp = row['Author'].split(";")
                author_id_list = []
                for author in author_list_tmp:
                    author_id_list.append(author_collection.find({"author": author.strip()})[0]["_id"])
                dict1["author_id"] = author_id_list

                publisher_id_list = []
                publisher_list_tmp = row['publisher'].split(";")
                for publisher in publisher_list_tmp:
                    publisher_id_list.append(publisher_collection.find({"publisher": publisher.strip()})[0]["_id"])
                dict1["publisher_id"] = publisher_id_list
                result = book_collection.insert_one(dict1)
                dict2["_id"] = result.inserted_id
                dict2["quantity"] = row["quantity"]
                inventory_collection.insert_one(dict2)

        cursor = book_collection.find({})
        for document in cursor:
            #pprint(document)
            pass

        cursor = inventory_collection.find({})
        for document in cursor:
            #pprint(document)
            pass

        self.db.customers.drop()
        customers_collection = self.db.customers
        with open("database/customer.csv", newline='') as csvfile:
            customersreader = csv.DictReader(csvfile, delimiter=',')

            for row in customersreader:
                dict1 = {}
                dict1["name"] = row["Name"]
                dict1["email_address"] = row["email_address"]
                dict1["address"] = row["address"]
                dict1["phone_number"] = row["phone number"]
                customers_collection.insert_one(dict1)

        cursor = customers_collection.find({})
        for document in cursor:
            #pprint(document)
            pass

        self.db.order.drop()
        order_collection = self.db.order
        with open("database/order.csv", newline='') as csvfile:
            orderreader = csv.DictReader(csvfile, delimiter=',')

            for row in orderreader:
                #print(row)
                dict1 = {}
                book_id_list = []
                # email_addr=row["userid"]
                # isbn_list_tmp=row['ISBN-13'].split(";")
                # for isbn in isbn_list_tmp:
                #     book_id_list.append(book_collection.find({"ISBN-13":isbn})[0]["_id"])
                # dict1["customer_id"]=customer_collection.find({"email_address":email_addr})[0]["_id"]
                dict1["order_id"] = row["order_id"]
                dict1['email'] = row["email"]
                dict1['title'] = row["title"]
                dict1["amount"] = row["amount"]
                dict1["created_time"] = row["created_time"]
                dict1['status'] = row["status"]
                dict1["completed_time"] = row["completed_time"]
                #print(dict1)
                order_collection.insert_one(dict1)

        cursor = order_collection.find({})
        for document in cursor:
            #pprint(document)
            pass

        ## creating authentication collection for login_id,salt,password collections
        self.db.auth.drop()
        login_collection = self.db.authentication
        with open('database/login.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                #print("type",type(row), "data", row)
                #print('email_address:', row['email_address'], 'salt:', row['salt'], 'password:', row['password'])
                #print(hashlib.sha256(str(row['salt']+hashlib.md5('password'.encode('utf-8')).hexdigest()).encode('utf-8')).hexdigest())
                row['password'] = hashlib.sha256(str(row['salt']+hashlib.md5('password'.encode('utf-8')).hexdigest()).encode('utf-8')).hexdigest()
                login_collection.insert_one(dict(row))


    def populate_db_json(self, collection, jfile):
        """
        read json from a file and populate the db
        """
        pass

if __name__ == '__main__':
    pymondb = APymongodb(test=True)
    pymondb.create_db_from_csv()
