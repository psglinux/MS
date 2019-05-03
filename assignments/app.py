# app.py

import bookapi
from flask import Flask
import pymongo
import mongomock

app = Flask(__name__)
app.config.from_object(__name__)

mongodb_uri="mongodb"

@app.route('/')
def hello_world():
    return '<h1 align=center>Hello, Welcome to the webserver of team ELFs</h1>'

@app.route('/getbook', methods=['GET'])
def get_all_books():
    books=[]
    print("app.testing:", app.testing)
    if app.testing:
        db = mongomock.MongoClient()['test_database']
        db.book.insert_one({'_id': '1', 'title': 'A test book', 'ISBN-10': '111-1234567'})
        db.book.insert_one({'_id': '2', 'title': 'Another test book', 'ISBN-13': '113-131313'})
        db.book.insert_one({'_id': '3', 'title': 'A rare book', 'ISBN-10': '113-145313'})
        db.book.insert_one({'_id': '4', 'title': 'A Rarest of Rare book', 'ISBN-13': '113-1545313'})
        db.inventory.insert_one({'_id': '1', 'id': '1', 'quantity': 5})
        db.inventory.insert_one({'_id': '2', 'id': '2', 'quantity': 0})
        db.inventory.insert_one({'_id': '3', 'id': '4', 'quantity': 1})
        db.inventory.insert_one({'_id': '4', 'id': '4', 'quantity': 10})
    else:
        db = pymongo.MongoClient(mongodb_uri)['test_database']

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
