# app.py

import bookapi
from flask import Flask

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def hello_world():
    return '<h1 align=center>Hello, Welcome to the webserver of team ELFs</h1>'

@app.route('/getbook', methods=['GET'])
def get_all_books():
    return str(["book1", "book2"])

@app.route('/getbook/<int:isbn_no>', methods=['GET'])
def get_book_by_isbn(isbn_no):
    return str({"book":"bbc", "isbn":"zbc"})


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0')
