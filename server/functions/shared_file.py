from functions import database as db 
from functions.result import Result
from functions.file import File

class SharedFile:
    def __init__(self, sharingId):
        fileData = db.get_data( "sharedFiles", { "sharingId": sharingId })
        
        self.sharingId = fileData[0]
        self.sharedFileId = fileData[1]
        self.transmitterId = fileData[2]
        self.recieverId = fileData[3]
        self.key = fileData[4]

    def __str__( self ):
        return f'{{"sharingId": "{self.sharingId}", "fileId": "{self.sharedf}","transmitterId": "{self.transmitterId}", "recieverId": "{self.recieverId}", "key": "{self.key}"}}'
    
    def __repr__( self ):
        return f'{{"sharingId": "{self.sharingId}", "fileId": "{self.sharedFileId}","transmitterId": "{self.transmitterId}", "recieverId": "{self.recieverId}", "key": "{self.key}"}}'
    
    @classmethod
    def share(self, file: File, recieverId: int, key: str) -> Result:
        try:
            db.insert_data("sharedFiles", {
                "sharingId": None,
                "sharedFileId": file.fileId,
                "transmitterId": file.userId,
                "recieverId": recieverId,
                "key": key
            })
            return Result(200, "Archivo compartido con éxito", True, {"fileId": file.fileId, "transmitterId": file.userId, "recieverId": recieverId, "key": key})
        except:
            return Result(500, "Error en el servidor al compartir fichero", False)
    
    @classmethod
    def getUsersSharedTo(self, file_id: int) -> Result:
        # Obtiene todas las comparticiones del fichero con el id facilitado
        shared_files: list[dict] = db.get_data_with_map( "sharedFiles", { "sharedFileId": file_id })

        users: list = []
        # Va guardando los usuarios a los que se ha compartido ese fichero en una lista
        for file in shared_files:
            users.append(db.get_data_with_map( "users", { "userId": file["recieverId"] })[0])
        
        return Result(200, "Usuario a los que se a compartido el archivo obtenidos con éxito", True, {"users": users})

    def delete(self) -> Result:
        try:
            db.remove_data("sharedFiles", {"sharingId": self.sharingId})
            return Result(200, "Archivo dejado de compartir con éxito", True)
        except:
            return Result(500, "Error del servidor al dejar de compartir archivo", False)
