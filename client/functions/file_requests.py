import json
import requests

def upload_file(aesKey: str, publicRSA: str, privateRSA: str, userId: int, localFilePath: str, fileType: str):
    payload = {
        "aesKey": aesKey,
        "publicRSA": publicRSA,
        "privateRSA": privateRSA,
        "userId": userId,
        "fileType": fileType
    }
    
    try:
        # Diccionario con los ficheros a subir. Cada uno va asociado con un nombre, en este caso 'fichero'
        files = {'fichero': open(localFilePath,'rb')}

        # Envia petición POST con los ficheros a subir
        #TODO: Usar variable global server
        r = requests.post('http://localhost:5000/upload', files=files, data=payload)

        # Cierra el fichero
        files['fichero'].close()

        # Devuelve la info devuelta por el server
        return json.loads(r.text)
    except:
        print("Error al subir el fichero")
        return None

def download_file(fileId: int, savePath: str):
    # Envia petición GET para descargar un fichero
    #TODO: Usar variable global server
    r = requests.get(f'http://localhost:5000/download/{fileId}')

    # Guarda el contenido de la respuesta en el fichero filePath
    try:
        file = open(savePath, 'wb')
        file.write(r.content)
        file.close()
    except:
        print("Error al descargar y guardar el fichero")
        
def get_file_info(fileId: int):
    # Envia peticion GET para obtener la informacion de un fichero
    #TODO: Usar variable global server
    r = requests.get(f'http://localhost:5000/get-file-info/{fileId}')
    
    return json.loads(r.text)
