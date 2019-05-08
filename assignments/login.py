# login.py
from flask import Flask
login = Flask(__name__)

@login.route('/')
def hello_world():
    return 'login Flask Dockerized app'

#by default the app run on port 5000
if __name__ == '__main__':
    login.run(debug=True,host='0.0.0.0')
