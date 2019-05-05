# app.py

import bookapi
import addorderapi
from flask import Flask
import pymongo
import mongomock
from flask import jsonify
from flask import request
from flask import json


from apymongodb import APymongodb
import bson

app = Flask(__name__)
app.config.from_object(__name__)

mongodb_uri="mongodb"

def mock_book_mongo_db():
    """
    create a mock db for usint testing.
    """
    mock_pymondb = APymongodb(test=True)
    mock_pymondb.create_db_from_csv()
    return mock_pymondb.db

def real_mongo_db():
    return pymongo.MongoClient(mongodb_uri)['test_database']

def get_db_instance():
    if app.testing:
        db = mock_book_mongo_db()
    else:
        db = real_mongo_db()

    return db

@app.route('/')
def hello_world():
    """
    default route for the Team Elf's home page
    """
    return '<h1 align=center>Hello, Welcome to the webserver of team ELFs</h1>'

@app.route('/getbook', methods=['GET'])
def get_all_books():
    books=[]
    #print("app.testing:", app.testing)

    db = get_db_instance()

    for book in bookapi.get_available_books(db):
        #print("book", str(book))
        books.append(book)
    #print(books)
    return bson.json_util.dumps(books)


@app.route('/getbook/<string:isbn_no>', methods=['GET'])
def get_book_by_isbn(isbn_no):
    db = get_db_instance()
    book = bookapi.get_book_with_isbn(isbn_no, db)
    #print("book retrieved:", type(book))
    #print("book", (book))
    return bson.json_util.dumps(book)

@app.route('/addorder', methods = ['POST'])
def app_message():
    if not request.json:
        return "415 Unsupported Media Type ;)"
    elif 'email' not in request.json:
        return "No email key  ;)"
    elif 'title' not in request.json:
        return "No title key  ;)"
    elif 'amount' not in request.json:
        return "No amount key  ;)"
    else:
        db = get_db_instance()
        order = addorderapi.Order(request.json['email'], request.json['title'], request.json['amount'])
        order_info = addorderapi.create_order(db, order)
        return bson.json_util.dumps(order_info)


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0')
