from flask import Flask
from functions.user import User
import json

app = Flask(__name__)

@app.route("/users")
def hello_world():
    users = json.loads(str(User.getAllUsers()))
    return users