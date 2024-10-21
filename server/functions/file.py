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
        self.publicRSA       = fileData[5]
        self.privateRSA      = fileData[6]
        self.date            = fileData[7]
        self.fileType        = fileData[8]

    def __str__( self ):
        return f'{{"fileId": "{self.fileId}", "userId": "{self.userId}","fileName": "{self.fileName}", "encryptedFile": "{self.encryptedFile}", "aesKey": "{self.aesKey}", "publicRSA": "{self.publicRSA}", "privateRSA": "{self.privateRSA}", "date": "{self.date}", "fileType": "{self.fileType}"}}'
    
    def __repr__( self ):
        return f'{{"fileId": "{self.fileId}", "userId": "{self.userId}","fileName": "{self.fileName}", "encryptedFile": "{self.encryptedFile}", "aesKey": "{self.aesKey}", "publicRSA": "{self.publicRSA}", "privateRSA": "{self.privateRSA}", "date": "{self.date}", "fileType": "{self.fileType}"}}'
    
    @classmethod
    def upload(self, file: FileStorage, path: str, aesKey: str, publicRSA: str, privateRSA: str, userId: int) -> Result:
        filename = secure_filename(file.filename)
        try:
            file.save(os.path.join(path, filename))
            db.insert_data("files", {
                "fileId": None,
                "userId": userId,
                "fileName": filename,
                "encryptedFile": os.path.join(path, filename),
                "aesKey": aesKey,
                "publicRSA": publicRSA,
                "privateRSA": privateRSA,
                "date": 'esto se podría poner solo',
                "fileType": filename.split('.')[-1] # Extension del fichero
            })
            return Result(200, "Fichero guardado con éxito", True)
        except:
            return Result(500, "Error al guardar el fichero", False)
        
    @classmethod
    def download(self, path: str, file_id: int) -> Response:
        fileData = db.get_data( "files", { "fileId": file_id })
        return send_from_directory(path, secure_filename(fileData[2]))

