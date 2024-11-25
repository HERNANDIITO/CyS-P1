from datetime import datetime
from functions import database as db 
import os
from flask import Response, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from functions.result import Result

class File:
    def __init__(self, fileId):
        fileData = db.get_data( "files", { "fileId": fileId })
        
        self.fileId          = fileData[0]
        self.userId          = fileData[1]
        self.fileName        = fileData[2]
        self.encryptedFile   = fileData[3]
        self.aesKey          = fileData[4]
        self.date            = fileData[5]
        self.fileType        = fileData[6]
        self.signature        = fileData[7]

    def __str__( self ):
        return f'{{"fileId": "{self.fileId}", "userId": "{self.userId}","fileName": "{self.fileName}", "encryptedFile": "{self.encryptedFile}", "aesKey": "{self.aesKey}", date": "{self.date}", "fileType": "{self.fileType}", "signature": "{self.signature}"}}'
    
    def __repr__( self ):
        return f'{{"fileId": "{self.fileId}", "userId": "{self.userId}","fileName": "{self.fileName}", "encryptedFile": "{self.encryptedFile}", "aesKey": "{self.aesKey}", "date": "{self.date}", "fileType": "{self.fileType}", "signature": "{self.signature}"}}'
    
    @classmethod
    def upload(self, file: FileStorage, path: str, aesKey: str, userId: int, fileType: str, fileName: str, signature: str) -> Result:
        secureFilename = secure_filename(fileName)
        try:
            timestamp_str = datetime.now().timestamp().__str__()
            file.save(os.path.join(path, timestamp_str + secureFilename))
            db.insert_data("files", {
                "fileId": None,
                "userId": userId,
                "fileName": secureFilename,
                "encryptedFile": timestamp_str + secureFilename,
                "AESKey": aesKey,
                "date": datetime.today().strftime('%Y-%m-%d %H:%M:%S'),
                "fileType": fileType,
                "signature": signature
            })
            return Result(200, "Fichero guardado con éxito", True)
        except:
            return Result(500, "Error al guardar el fichero", False)
        
    @classmethod
    def download(self, path: str, file_id: int) -> Response:
        fileData = db.get_data( "files", { "fileId": file_id })
        return send_from_directory(path, secure_filename(fileData[3]))
    
    @classmethod
    def getFileData(self, file_id: int) -> Response:
        try:
            file = File(file_id)
            return Result(200, "Datos del fichero obtenidos con éxito", True, {"fileId": file.fileId, "userId": file.userId,"fileName": file.fileName, "encryptedFile": file.encryptedFile, "aesKey": file.aesKey, "date": file.date, "fileType": file.fileType, "signature": file.signature})
        except:
            return Result(404, "No existe un fichero con el id facilitado", False)
    
    def delete(self) -> Result:
        try:
            db.remove_data("files", {"fileId": self.fileId})
            return Result(200, "Archivo eliminado con éxito", True)
        except:
            return Result(500, "Error del servidor al borrar archivo", False)
