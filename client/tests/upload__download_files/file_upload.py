import requests

# Diccionario con los ficheros a subir. Cada uno va asociado con un nombre, en este caso 'fichero'
files = {'fichero': open('image.png','rb')}

# Envia petición POST con los ficheros a subir
r = requests.post('http://127.0.0.1:5000/upload-test', files=files)