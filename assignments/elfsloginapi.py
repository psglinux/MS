import requests

login_uri="login_flask:5000"

def login_api():
    r = requests.get(login_uri)
    print("response:", r.text)
    pass

if __name__ == "__main__":
    login_api()

