import json
import requests
from  functions.result import Result
from functions.consts import server

def upload_file(aesKey: str, userId: int, localFilePath: str, fileType: str, fileName: str, signature: str):
    payload = {
        "aesKey": aesKey,
        "userId": userId,
        "fileType": fileType,
        "fileName": fileName,
        "signature": signature
    }
    
    try:
        # Diccionario con los ficheros a subir. Cada uno va asociado con un nombre, en este caso 'fichero'
        files = {'fichero': open(localFilePath,'rb')}

        # Envia petición POST con los ficheros a subir
        r = requests.post(f'{server}/upload', files=files, data=payload)

        # Cierra el fichero
        files['fichero'].close()

        # Devuelve la info devuelta por el server
        return json.loads(r.text)
    except:
        return Result(500, "Error al subir el archivo, inténtelo de nuevo", False, "")

def download_file(fileId: int, savePath: str):
    # Envia petición GET para descargar un fichero
    r = requests.get(f'{server}/download/{fileId}')

    # Guarda el contenido de la respuesta en el fichero filePath
    try:
        file = open(savePath, 'wb')
        file.write(r.content)
        file.close()
    except:
        return Result(500, "Error al descargar y guardar el fichero", False, "")
        
def get_file_info(fileId: int):
    # Envia peticion GET para obtener la informacion de un fichero
    r = requests.get(f'{server}/get-file-info/{fileId}')
    
    return json.loads(r.text)

def get_sharedfile_info(sharingId: int):
    # Envia peticion GET para obtener la informacion de un fichero
    r = requests.get(f'{server}/get-shared-info/{sharingId}')
    r = json.loads(r.text)
    
    return r

def share_file(sharedFileId, userId, recieverId, encryptedAESKeyforReciever):
    try:
        r = requests.post(f'{server}/share-file', json = {
            "file_id": sharedFileId,
            "reciever_id": recieverId,
            "key": encryptedAESKeyforReciever,
            "user_id": userId
        })
        
        return r
    except Exception as e:
        return Result(500, f"Error al compartir archivo: {e}", False, "")
