# app.py
from flask import Flask
app = Flask(__name__)
@app.route('/')
def hello_world():
    return '<h1 align=center>Hello, Welcome to the Project of team ELFs</h1>'
if __name__ == '__main__':
    app.run(host='0.0.0.0')
