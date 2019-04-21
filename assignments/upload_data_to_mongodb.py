import csv
from pymongo import MongoClient
import sys
from pprint import pprint

client = MongoClient()
client = MongoClient('localhost', 27017)
db = client.test_database

#Find the unique authors and publishers
author_list=[]
publisher_list=[]
with open("book.csv",newline='') as csvfile:
    bookreader = csv.DictReader(csvfile, delimiter=',')
    for row in bookreader:
        author_list_tmp=row['Author'].split(";")
        for author in author_list_tmp:
            if author.strip() not in author_list:
                author_list.append(author.strip())
        publisher=row['publisher'].strip()
        if publisher not in publisher_list:
                publisher_list.append(publisher)
#print(author_list)
#print(publisher_list)

#creating author collection and create documents
db.author.drop()
author_collection = db.author
db.publisher.drop()
publisher_collection = db.publisher

for author_name in author_list:
    print(author_name)
    author_dict={"author":author_name}
    author_collection.insert_one(author_dict)
cursor = author_collection.find({})
for document in cursor: 
    pprint(document)
for publisher_name in publisher_list:
    print(publisher_name)
    publisher_dict={"publisher":publisher_name}
    publisher_collection.insert_one(publisher_dict)
cursor = publisher_collection.find({})
for document in cursor: 
    pprint(document)
print(db.collection_names())


db.book.drop()
book_collection = db.book
with open("book.csv",newline='') as csvfile:
    bookreader = csv.DictReader(csvfile, delimiter=',')
    
    for row in bookreader:
        dict1={}
        print(row)
        dict1["title"]=row["Title"]
        dict1["ISBN-13"]=row["ISBN-13"]
        dict1["ISBN-10"]=row["ISBN-10"]
        dict1["review_count"]=row["Reviews"]
        dict1["description"]=row["Book Description"]
        dict1["release_id"]=row["Release date"]
        author_list_tmp=row['Author'].split(";")
        author_id_list=[]
        for author in author_list_tmp:
           author_id_list.append(author_collection.find({"author":author.strip()})[0]["_id"])
        dict1["author_id"]=author_id_list

        publisher_id_list=[]
        publisher_list_tmp=row['publisher'].split(";")
        for publisher in publisher_list_tmp:
           publisher_id_list.append(publisher_collection.find({"publisher":publisher.strip()})[0]["_id"])
        dict1["publisher_id"]=publisher_id_list
        book_collection.insert_one(dict1)

cursor = book_collection.find({})
for document in cursor: 
    pprint(document)
