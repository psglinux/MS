import sys
import pymongo


def get_available_books(db):
    available_books = []
    try:
        for record in db.inventory.find({}):
            book_id = record['_id']
            qty = record['quantity']
            if int(qty) <= 0:
                continue
            book = db.book.find_one({'_id': book_id})
            book['quantity'] = qty
            available_books.append(book)
    except Exception as e:
        print("exception:"+ str(e))
    return available_books

if __name__ == "__main__":
    argv = sys.argv
    if len(argv) < 2:
        print("Usage: python list_books.py mongodb_uri")
        exit(-1)

    mongodb_uri = argv[1]

    db = pymongo.MongoClient(mongodb_uri)['test_database']
    for book in get_available_books(db):
        print(book['title'], book['quantity'])
