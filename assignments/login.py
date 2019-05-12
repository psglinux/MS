# login.py
from flask import Flask
from flask import jsonify
from flask import request
from flask import Response
import json
import hashlib
from apymongodb import APymongodb
from app import get_db_instance, mock_book_mongo_db, real_mongo_db

login = Flask(__name__)

mongodb_uri="mongodb"

@login.route('/')
def hello_world():
    return 'login Flask Dockerized app'

@login.route('/login', methods = ['POST'])
def login_user():
    """
    The login api returns wither a success or a failure as a jason to a caller app
    """
    try:
        #print("request data:", json.loads(request.data))
        r = json.loads(request.data)
        db = get_db_instance()
        l_data = db.authentication.find_one({'email_address': r['email_address']})
        #print('retrieved login data:',l_data)
        #calculate sha256 with salt + md5 hash, compare with the retrieved password
        passwd = hashlib.sha256(str(l_data['salt'] + r['password']).encode('utf-8')).hexdigest()
        #print ('calculated password hash:', passwd)
        #print ('database   password hash:', l_data['password'])
        if passwd == l_data['password']:
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'error'})
    except Exception as e:
        print("exception:", str(e))
    return jsonify({'status': 'internal error'})

    pass

#by default the app run on port 5000
if __name__ == '__main__':
    login.run(debug=True,host='0.0.0.0')
