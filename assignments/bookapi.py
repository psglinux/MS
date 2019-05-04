import sys
import pymongo

def find_author(_id, db):
    try:
        auth = db.author.find_one({'_id': _id[0]})
        #print(auth['author'])
        return auth['author']
    except Exception as e:
        print("exception:"+ str(e))
        return None

def find_publisher(_id, db):
    try:
        pub = db.publisher.find_one({'_id': _id[0]})
        #print(pub['publisher'])
        return pub['publisher']
    except Exception as e:
        print("exception:"+ str(e))
        return None

def find_inventory(_id, db):
    try:
        inv = db.inventory.find_one({'_id': _id})
        #print(inv['quantity'])
        return inv['quantity']
    except Exception as e:
        print("exception:"+ str(e))
        return 0

def get_available_books(db):
    available_books = []
    try:
        for record in db.inventory.find({}):
            book_id = record['_id']
            qty = record['quantity']
            if int(qty) <= 0:
                continue
            book = db.book.find_one({'_id': book_id})
            book['quantity'] = find_inventory(book['_id'], db)
            book['author'] = find_author(book['author_id'], db)
            book['publisher'] = find_publisher(book['publisher_id'], db)
            available_books.append(book)
    except Exception as e:
        print("exception:"+ str(e))
    return available_books

def get_book_with_isbn(_no, db):
    print("_no",_no)
    print("tyep(_no)",type(_no))
    try:
        book = db.book.find_one({"$or": [{"ISBN-10": _no}, {"ISBN-13": _no}]})
        if book is not None:
            #print("book:", book['_id'])
            book['quantity'] = find_inventory(book['_id'], db)
            book['author'] = find_author(book['author_id'],db)
            book['publisher'] = find_publisher(book['publisher_id'],db)
            #print(str(book))
            return book
    except Exception as e:
        print("exception:"+ str(e))

    return ([])


if __name__ == "__main__":
    argv = sys.argv
    if len(argv) < 2:
        print("Usage: python list_books.py mongodb_uri")
        exit(-1)

    mongodb_uri = argv[1]

    db = pymongo.MongoClient(mongodb_uri)['test_database']
    for book in get_available_books(db):
        print(book['title'], book['quantity'])
