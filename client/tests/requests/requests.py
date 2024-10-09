import requests, json

r = requests.get('http://127.0.0.1:5000/users')

register = requests.post('http://127.0.0.1:5000/register', json = {
    "user": "Prueba",
    "pass": "Contraseña prueba"
    })

print(json.loads(r.text)[1]["user"])
print(json.loads(register.text))