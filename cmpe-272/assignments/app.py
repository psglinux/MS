# app.py

import bookapi
import addorderapi
from flask import Flask
import pymongo
import mongomock
import requests
from flask import jsonify
from flask import request
from flask import Response
from flask import abort
from flask import json,jsonify, make_response,session
from flask import render_template,request,redirect,url_for
from apymongodb import APymongodb
import bson
import json
import jwt
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


mongodb_uri="mongodb"
login_uri="login-flask"

endpoint_access = {'N': ['login', 'getbook', 'order', 'addorder'],
                   'S': ['login', 'getbook', 'order', 'addorder', 'getorders', 'fullfillorder']}

def check_endpoint_access(db, email, ep):
    l_data = db.authentication.find_one({'email_address':  email})
    if l_data :
        if ep in endpoint_access[l_data['role']]:
            return True
    return False

def mock_book_mongo_db():
    """
    create a mock db for usint testing.
    """
    mock_pymondb = APymongodb(test=True)
    mock_pymondb.create_db_from_csv()
    return mock_pymondb.db


def real_mongo_db():
    print(mongodb_uri)
    return pymongo.MongoClient(mongodb_uri)['test_database']


def get_db_instance():
    print("Inside get db instance")
    print(app.testing)
    if app.testing:
        db = mock_book_mongo_db()
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
    return '<h1 align=center>Hello, Welcome to the webserver of team ELFs</h1>'


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
            #print(email_addr, ",", password)
            rcv_login_req={'email_address':email_addr, 'password':password}
            # request the login-app to authenticate the user
            #pdata1 = {'email_address':'95f7vcnewd8@iffymedia.com', 'password':'5f4dcc3b5aa765d61d8327deb882cf99'}
            #rcv_login_req = {'email_address':'95f7vcnewd8@iffymedia.com', 'password':'5f4dcc3b5aa765d61d8327deb882cf99'}
            #r = requests.post('http://login-flask:5000/login', data=json.dumps(pdata1), headers=headers)
            headers = {'content-type': 'application/json'}
            r = requests.post('http://login-flask:5000/login', data=bson.json_util.dumps(rcv_login_req), headers=headers)
            print("send request", dir(r))
            #r = requests.get('http://login-flask:5000/')
            #print("response:", dir(r))
            print("response.text:", r.text)
            print("response.status_code", r.status_code)
            print("response.json", r.json)
            # TODO: Return the JWT here
            session['Authorization']=json.loads(r.text)['auth_token']
            return redirect(url_for('order_books'))
            #return redirect(url_for('get_all_books'))
            #return '<h1>'+str(r.status_code)+'</h1>'+'<h2>'+r.text+'</h2>+'
         except Exception as e:
            print("exception:", str(e))
            #return '<h1>'+"error"+'</h1>'
    return render_template('login.html', error=error)

@app.route('/getbook', methods=['GET'])
def get_all_books():
    db = get_db_instance()
    #if request.data=='':
    #    request=None
    auth_status = check_auth_token(request,db)
    if auth_status == 'success':
        books=[]
        #print("app.testing:", app.testing)
        for book in bookapi.get_available_books(db):
            #print("book", str(book))
            books.append(book)
        print(books)
        #return bson.json_util.dumps(books)
        return render_template('getbook.html',response=books)
    else:
        return redirect(url_for('app_login'))
        return '<h1>'+auth_status+'</h1>'


@app.route('/order', methods=['GET','POST'])
def order_books():

    books=[]
    order_dict={}
    db = get_db_instance()
    auth_status = check_auth_token(request, db)
    if auth_status == 'success':
        if request.method=="POST":
            print("Inside post")
            book_id_list=request.form.getlist('book_id_list')
            quantity_list=request.form.getlist('quantity_list')
            form_dict=dict(request.form)
            del form_dict["submit_order"]
            del form_dict["book_id_list"]
            order_dict["order"]=[]
            order_dict["email"]="95f7vcnewd8@iffymedia.com"
            for id in book_id_list:
               tmp_dict={}
               tmp_dict["book_id"]=id
               tmp_dict["quantity"]=form_dict[id][0]
               order_dict["order"].append(tmp_dict)
            print(order_dict)
            order = addorderapi.Order(order_dict)
            print(order)
            order_info = addorderapi.create_order(db, order)
            return bson.json_util.dumps(order_info)
            #return redirect(url_for('addorder',response=json.dumps(str(order_dict2))),code=307)

        #print("app.testing:", app.testing)

        for book in bookapi.get_available_books(db):
            #print("book", str(book))
            books.append(book)
        print(books)
        #return bson.json_util.dumps(books)
        return render_template('order.html',response=books)
    else:
        return redirect(url_for('app_login'))
        return '<h1>' + auth_status + '</h1>'


@app.route('/getbook/<string:isbn_no>', methods=['GET'])
def get_book_by_isbn(isbn_no):
    db = get_db_instance()
    auth_status = check_auth_token(request, db)
    if auth_status == 'success':
        book = bookapi.get_book_with_isbn(isbn_no, db)
        #print("book retrieved:", type(book))
        #print("book", (book))
        return bson.json_util.dumps(book)
    else:
        return '<h1>' + auth_status + '</h1>'


@app.route('/addorder', methods = ['POST'])
def addorder():
    db = get_db_instance()
    return session
    auth_status = check_auth_token(request, db)
    if auth_status == 'success':
        if not request.json:
            return "415 Unsupported Media Type ;)"
        elif 'email' not in request.json:
            return "No email key  ;)"
        elif 'title' not in request.json:
            return "No title key  ;)"
        elif 'amount' not in request.json:
            return "No amount key  ;)"
        else:
            db = get_db_instance()
            order = addorderapi.Order(request.json['email'], request.json['title'], request.json['amount'])
            order_info = addorderapi.create_order(db, order)
            return bson.json_util.dumps(order_info)
    else:
        return '<h1>' + auth_status + '</h1>'


'''
PUT orders/number: "fulfills the order" - i.e.
adjusts the inventory to account for the books shipped for this order.
'''
@app.route('/getorders', methods=['GET'])
def get_orders():
    """
    get all the orders that have been placed. This is to be used for the admin user
    """
    db = get_db_instance()
    auth_status = check_auth_token(request, db, ep="getorders")
    if auth_status == 'success':
        db = get_db_instance()
        orders = db.orders.find()
        print(orders)
        return render_template('getorder.html',response=orders)
    else:
        return '<h1>' + auth_status + '</h1>'


@app.route('/fullfillorder', methods=['POST'])
def fullfill_book_order():
    print("post data", request.form['order_id'])
    order_id=request.form['order_id']
    # Find the order from the db which matches order ID
    if not order_id:
        print("Order is None")
        abort(404)
    db = get_db_instance()
    if not db:
        print("DB NOT found")
        abort(400)

    order = None
    # Then create an order object corresponding to that it.
    order = db.orders.find_one({'order_id':int(order_id)})
    print("order:", order)

    if not order:
        print("No such order")
        abort(404)
    # Then invoke process_order
    val=addorderapi.process_order(db, order_id)
    return get_orders()


@app.route('/processorder/<int:order_id>', methods=['PUT'])
def process_book_order(order_id):
    print(type(order_id))
    # Find the order from the db which matches order ID
    if not order_id:
        print("Order is None")
        abort(404)
    db = get_db_instance()
    if not db:
        print("DB NOT found")
        abort(400)

    order = None
    # Then create an order object corresponding to that it.
    order = db.orders.find_one({'order_id':int(order_id)})

    if not order:
        print("No such order")
        abort(404)
    # Then invoke process_order
    val=addorderapi.process_order(db, order_id)
    return val


if __name__ == '__main__':
#    app = Flask(__name__)
    app.run(host='127.0.0.1',port=5000,debug=True)
