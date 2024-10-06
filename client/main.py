import requests, json

r = requests.get('http://127.0.0.1:5000/users')

for s in json.loads(r.text):
    print(s,"\n")