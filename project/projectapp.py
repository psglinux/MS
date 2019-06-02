# app.py

import pprint
import json
import bson
import jwt

import pymongo
import mongomock
import requests
from flask import Flask
from flask import jsonify
from flask import request
from flask import Response
from flask import abort
from flask import json,jsonify, make_response,session
from flask import render_template,request,redirect,url_for
from apymongodb import APymongodb
import reviewapi
import query
SECRET_KEY = "Secret Key"

#app = Flask(__name__)
#app.config.from_object(__name__)
# create flask instance
def create_app():
    app=Flask(__name__)
    return app
app=create_app()

app = Flask(__name__)
app.config.from_object(__name__)


mongodb_uri="project-mongodb"
login_uri="porject-login-flask"

endpoint_access = {'N': ['login'],
                   'S': ['login']}

def check_endpoint_access(db, email, ep):
    l_data = db.authentication.find_one({'email_address':  email})
    if l_data :
        if ep in endpoint_access[l_data['role']]:
            return True
    return False

def mock_project_mongo_db():
    """
    create a mock db for usint testing.
    """
    mock_pymondb = APymongodb(test=True)
    mock_pymondb.create_db_from_csv()
    mock_pymondb.create_auth_db()
    return mock_pymondb.db


def real_mongo_db():
    print(mongodb_uri)
    return pymongo.MongoClient(mongodb_uri)['client_database']


def get_db_instance():
    print("Inside get db instance")
    print(app.testing)
    if app.testing:
        db = mock_project_mongo_db()
    else:
        db = real_mongo_db()

    return db


def check_auth_token(request,db, ep=None):
    if 'Authorization' in session.keys():
         print(session.keys())
         auth_token=session['Authorization']
    else:
         auth_token=""
    if auth_token:
        try:
            payload = jwt.decode(auth_token,
                                 SECRET_KEY,
                                 algorithm="HS256")
            db = get_db_instance()
            l_data = db.authentication.find_one({'email_address':  payload['sub']})
            if l_data:
                if ep is not None:
                    if not check_endpoint_access(db, payload['sub'], ep):
                        return 'error'
                return 'success'
            else:
                return 'error'
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
    else:
        return 'error: no jwt token provided'


@app.route('/',methods=['GET'])
def hello_world():
    """
    default route for the Team Elf's home page
    """
    return '<h1 align=center>Hello, Welcome to the Project webserver of team ELFs</h1>'

@app.route('/login', methods=['POST','GET'])
def app_login():
    """
    the route for login. This will talk to a standalone app which is running in
    the container login-flask:5000
    """
    error=None
    if app.testing:
        return bson.json_util.dumps({'status': 'success'})
    else:
        print("received requests")
        if request.method == 'POST':
         try:
            #print("request data from browser:", request.data)
            #print("request data from browser:", json.loads(request.data))
            #rcv_login_req = json.loads(request.data)
            #print("request json from browser:", rcv_login_req)
            email_addr=request.form['username']
            password=request.form['password']
            print(email_addr, ",", password)
            rcv_login_req={'email_address':email_addr, 'password':password}
            # request the login-app to authenticate the user
            #pdata1 = {'email_address':'95f7vcnewd8@iffymedia.com', 'password':'5f4dcc3b5aa765d61d8327deb882cf99'}
            headers = {'content-type': 'application/json'}
            r = requests.post('http://project-login-flask:5000/login', data=bson.json_util.dumps(rcv_login_req), headers=headers)
            #print("send request", dir(r))
            #r = requests.get('http://login-flask:5000/')
            #print("response:", dir(r))
            print("response.text:", r.text)
            print("response.status_code", r.status_code)
            #print("response.json", r.json)
            # TODO: Return the JWT here
            session['Authorization']=json.loads(r.text)['auth_token']
            #return redirect(url_for('order_books'))
            #return render_template('login_success.html', error=error)
            return '<h1>'+"Success"+'</h1>'
         except Exception as e:
            print("exception:", str(e))
            #return '<h1>'+"error"+'</h1>'
    return render_template('login.html', error=error)

@app.route('/review/<string:listing_id>', methods=['GET'])
def get_review_by_id(listing_id):
    db = get_db_instance()
    auth_status = check_auth_token(request, db)
    if auth_status == 'success':
        reviews = reviewapi.get_review_with_listing_id(listing_id, db)
        print("reviews:", reviews)
        return render_template('reviews.html',response=reviews)
    else:
        return '<h1>' + auth_status + '</h1>'

@app.route('/loginsuccess', methods=['GET'])
def get_login_success():
    return render_template('login_success.html', error="")

# Test using -> curl -X POST -H 'Content-Type: application/json' http://127.0.0.1/getlistings -d '{"bedrooms":"5.0"}'
# See https://gist.github.com/subfuzion/08c5d85437d5d4f00e58
# Run project/run_proj.sh

#http://ec2-18-191-206-216.us-east-2.compute.amazonaws.com/getlistings?zipcode=3018&bedrooms=1&accomodates=0
@app.route('/getlistings', methods=['GET'])

def get_listings():
    def merge_dicts(x, y):
        z = x.copy()
        z.update(y)
        return z


    # XXX TODO How to check token using CURL ?
    #auth_status = check_auth_token(request, db)
    #if auth_status != 'success':
    #    return '<h1>' + auth_status + '</h1>'
    
    if request.method == 'GET':
        range_params={}
        error=None
        query_params = { 'country_code' : 'AU' }
        zipcode=request.args.get('zipcode')
        print(request.args)
        if zipcode is None:
            return render_template('test1.html', error=error)
        else:
            db = get_db_instance()

            results = {}
            query_params['zipcode']=int(request.args.get('zipcode'))
            price_max=request.args.get('price').strip()
            if price_max.startswith('$'):
               pass
            else:
               price_max="$"+price_max
               
            range_params['price'] =  { 'lo' : '$0.00', 'hi' : price_max}
            range_params['accomodates']={'lo': int(request.args.get('accomodates')),'hi':10}
            range_params['bedrooms']={'lo': int(request.args.get('bedrooms')),'hi':6}
            print("query_params",range_params,query_params)
            print(query.range_query(range_params,query_params,db))
            rv, r = query.range_query(range_params,query_params,db)
            if not rv:
                print("404")
                abort(404)
            results["results"] = r
            print(results)
            return render_template('listings.html',response=results)
            #return jsonify(results)



if __name__ == '__main__':
#    app = Flask(__name__)
    app.run(host='127.0.0.1',port=5000,debug=True)
