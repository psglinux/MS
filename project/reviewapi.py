import sys
import pymongo

def get_all_reviews(db):
    pass

def get_review_with_listing_id(_id, db):
    print("_id",_id)
    print("type(_id)",type(_id))
    _id = int(_id)
    rev_lst = []
    try:
        reviews = db.reviews.find({"listing_id": _id})
        if reviews is not None:
            #print("dir(reviews):", dir(reviews))
            #print("reviews:", reviews)
            for r in reviews:
                rev_lst.append(r)
            return rev_lst
    except Exception as e:
        print("exception:"+ str(e))
    return rev_lst



if __name__ == "__main__":
    argv = sys.argv
    if len(argv) < 2:
        print("Usage: python3.6 reviewapi.py  mongodb_uri <listing_id>")
        exit(-1)

    mongodb_uri = argv[1]
    listing_id = int(argv[2])

    db = pymongo.MongoClient(mongodb_uri)['client_database']
    print(get_review_with_listing_id(listing_id, db))
