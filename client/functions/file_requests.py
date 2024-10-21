import json
import requests

def upload_file(aesKey: str, publicRSA: str, privateRSA: str, userId: int, imgPath: str):
    payload = {
        "aesKey": aesKey,
        "publicRSA": publicRSA,
        "privateRSA": privateRSA,
        "userId": userId
    }
    
    try:
        # Diccionario con los ficheros a subir. Cada uno va asociado con un nombre, en este caso 'fichero'
        files = {'fichero': open(imgPath,'rb')}

        # Envia petición POST con los ficheros a subir
        #TODO: Usar variable global server
        r = requests.post('http://localhost:5000/upload', files=files, data=payload)

        # Cierra el fichero
        files['fichero'].close()

        # Devuelve la info devuelta por el server
        return json.loads(r.text)
    except:
        print("Error al subir la imagen")
        return None

def download_file(fileId: int, savePath: str = "downloadedImage.png"):
    # Envia petición GET para descargar un fichero
    #TODO: Usar variable global server
    r = requests.get(f'http://localhost:5000/download/{fileId}')

    # Guarda el contenido de la respuesta en el fichero downloadedImage.png
    try:
        open(savePath, 'wb').write(r.content)
    except:
        print("Error al descargar y guardar la imagen")
