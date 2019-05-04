# app.py

import bookapi
from flask import Flask
import pymongo
import mongomock
from flask import jsonify

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
    print("app.testing:", app.testing)

    db = get_db_instance()

    for book in bookapi.get_available_books(db):
        print(book['title'], book['quantity'])
        books.append(book)
    return bson.json_util.dumps(books)

@app.route('/getbook/<int:isbn_no>', methods=['GET'])
def get_book_by_isbn(isbn_no):
    db = get_db_instance()
    book = bookapi.get_book_with_isbn(isbn_no, db)
    print("book", type(book))
    if book is not None and '_id' in book.keys():
        del book['_id']
        del book['author_id']
        del book['publisher_id']
    return jsonify(book)


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0')
