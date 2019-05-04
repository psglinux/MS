# app.py

import bookapi
from flask import Flask
import pymongo
import mongomock
from apymongodb import APymongodb

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
    if app.testing:
        db = mock_book_mongo_db()
    else:
        db = real_mongo_db()

    for book in bookapi.get_available_books(db):
        print(book['title'], book['quantity'])
        books.append(book)
    return str(books)

@app.route('/getbook/<int:isbn_no>', methods=['GET'])
def get_book_by_isbn(isbn_no):
    return str({"book":"bbc", "isbn":"zbc"})


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0')
