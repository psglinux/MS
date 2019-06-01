from pymemcache.client import base
import json

memcachedhost='project-memcached'

def get_listing_review_id_from_cache(_id):
    print("retrieveing from memcached")
    try:
        client = base.Client((memcachedhost, 11211))
        key = 'reviews_'+str(_id)
        result = client.get(key)
        #print ("from memcached :", result)
        if result is None:
            return {'status': 'not-found'}
    except Exception as e:
        print("exception:" + str(e))
        return {'status': 'error'}
    return {'status':'success', 'data': json.loads(result)}

def update_listing_review_id_from_cache(_id, data):
    print("updating memcached")
    try:
        client = base.Client((memcachedhost, 11211))
        key = 'reviews_'+str(_id)
        print("key:", key)
        result = client.get(key)
        #print("result:", result)
        if result is None:
            print('setting the values in pymemcached')
            #print('data being set:', data)
            #print('data type:', type(data))
            client.set(key, json.dumps(data))
            print('setting the values in pymemcached successful')
    except Exception as e:
        print("exception:" + str(e))
        return {'status': 'error'}
    return {'status': 'success'}

