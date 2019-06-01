# login.py
from flask import Flask
from flask import jsonify
from flask import request, make_response
from flask import Response
import json
import hashlib
import datetime
import jwt
from apymongodb import APymongodb
from projectapp import get_db_instance, mock_project_mongo_db, real_mongo_db

login = Flask(__name__)

mongodb_uri="project-mongodb"
SECRET_KEY = "Secret Key"

def encode_auth_token(user_id):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=1000),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            SECRET_KEY,
            algorithm='HS256'
        )
    except Exception as e:
        return e


@login.route('/')
def hello_world():
    return 'login Flask Dockerized app'

@login.route('/login', methods = ['POST'])
def login_user():
    """
    The login api returns wither a success or a failure as a jason to a caller app
    """
    try:
        print("request data:", json.loads(request.data))
        r = json.loads(request.data)
        db = get_db_instance()
        l_data = db.authentication.find_one({'email_address': r['email_address']})
        print('retrieved login data:',l_data)
        # calculate sha256 with salt + md5 hash, compare with the retrieved password
        passwd = hashlib.sha256(str(l_data['salt'] + r['password']).encode('utf-8')).hexdigest()
        print ('calculated password hash:', passwd)
        print ('database   password hash:', l_data['password'])
        if passwd == l_data['password']:
            auth_token = encode_auth_token(l_data["email_address"])
            responseObject = {
                'status': 'success',
                'auth_token': auth_token.decode()
            }
            print(responseObject)
            # return jsonify(responseObject)
            return jsonify({'status': 'success','auth_token': auth_token.decode()})
        else:
            return jsonify({'status': 'error'})
    except Exception as e:
        print("exception:", str(e))
    return jsonify({'status': 'internal error'})
    pass

#by default the app run on port 5000
if __name__ == '__main__':
    login.run(debug=True,host='0.0.0.0')


