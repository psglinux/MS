#!/usr/bin/env python

import argparse
import os
from bottle import route, run, template
from bottle import get, post, request 

global http_port_number
global host_ip

def check_login(username, password):
    return False 

@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

@route('/listdir')
def listdir():
    return template('<b>{{name}}</b>!', name=os.listdir("."))

@get('/login') # or @route('/login')
def login():
    return '''
        <form action="/login" method="post">
            Username: <input name="username" type="text" />
            Password: <input name="password" type="password" />
            <input value="Login" type="submit" />
        </form>
    '''

@post('/login') # or @route('/login', method='POST')
def do_login():
    username = request.forms.get('username')
    password = request.forms.get('password')
    if check_login(username, password):
        return "<p>Your login information was correct.</p>"
    else:
        return "<p>Login failed.</p>"


def run_bottle_http_server():
    #
    run(host=host_ip, port=http_port_number)

def main():
    global http_port_number
    global host_ip
    parser = argparse.ArgumentParser(description="Run a bottle http server with a couple of rest api. \n\
                           current support rest support\n \
                              i. http://localhost/hello/<name>\n \
                             ii. http://localhost/listdir\n \
                            iii. http://localhost/login  (get and post)\n \
                            \n\
                            So for the suricata http filtering,\n \
                            we need to block the \n\
                            i. listdir key word in the url \n\
                           ii. hello/darknet")

    parser.add_argument('--ip', dest='localhost', default='localhost', type=str,
                       help='ip on which http server would be bound to')
    parser.add_argument('--port', dest='port', default=8080, type=int,
                       help='port number on which http server would be run')

    args = parser.parse_args()
    http_port_number = args.port
    host_ip=args.localhost
    run_bottle_http_server()

if __name__ == "__main__":
    main()

