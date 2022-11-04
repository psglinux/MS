import sys
import pymongo
import projectmemcached
import time

def get_all_reviews(db):
    pass


def get_review_with_listing_id(_id, db):
    #print("_id",_id)
    #print("type(_id)",type(_id))
    _id = int(_id)
    rev_lst = []
    start_time = time.time()

    try:
        reviews = projectmemcached.get_listing_review_id_from_cache(_id)
        if reviews['status'] is 'success':
            #print("dir(reviews):", dir(reviews))
            #print("reviews:", reviews)
            for r in reviews['data']:
                rev_lst.append(r)
            print("reviews returned from cache")
            print("--- memcached time taken : %s seconds ---" % (time.time() - start_time))
            return rev_lst
    except Exception as e:
        print("exception:"+ str(e))

    print('data not found in memcached for id:', _id)

    start_time = time.time()
    try:
        reviews = db.reviews.find({"listing_id": _id})
        if reviews is not None:
            #print("dir(reviews):", dir(reviews))
            #print("reviews:", reviews)
            for r in reviews:
                rev_lst.append(r)
            #update memcached
            print("--- mongodb time taken : %s seconds ---" % (time.time() - start_time))
            ret = projectmemcached.update_listing_review_id_from_cache(_id, rev_lst)
            if ret['status'] is 'success':
                print('memcached updated successfully id:', _id)
            else:
                print('memcached updated failed id:', _id)
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
