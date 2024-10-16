import requests, json
from ui import ui_prueba 

global server
server = "http://127.0.0.1:5000"
r = requests.get(server+'/users')

# for s in json.loads(r.text):
#     print(s,"\n")

print(json.loads(r.text)[1]["user"])

# ui_prueba.seleccionar_archivo()

