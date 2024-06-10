import requests

def get_token(email, password):
    json_data = {
        "email": email,
        "password": password
        }
    req = requests.post("http://127.0.0.1:8000/api/auth/token/", json=json_data)
    tokens = req.json()
    return tokens['access']

def create_employee(token):
    pass

email = "admin@admin.com"
password = "passforadmin"