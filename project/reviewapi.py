import sys
import pymongo

def get_all_reviews(db):
    pass

def get_review_with_listingid(_no, db):
    print("_no",_no)
    print("type(_no)",type(_no))
    """
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
    """
    pass



if __name__ == "__main__":
    argv = sys.argv
    if len(argv) < 2:
        print("Usage: python3.6 reviewapi.py  mongodb_uri")
        exit(-1)

    mongodb_uri = argv[1]

    db = pymongo.MongoClient(mongodb_uri)['client_database']
    """
    for book in get_available_books(db):
        print(book['title'], book['quantity'])
    """
