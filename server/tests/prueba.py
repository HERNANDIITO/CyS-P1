from flask import Flask, request
from functions.user import User
import json

app = Flask(__name__)

@app.get("/users")
def getAllUsers():
    users = json.loads(str(User.getAllUsers()))
    return users

@app.post("/register")
def registerUser():
    input_json = request.get_json(force=True) 
    print(input_json)
    return input_json

@app.get("/register/<param>")
def registerUser(param):
    print(param)
    return json.loads(param)