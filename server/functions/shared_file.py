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
        return f'{{"sharingId": "{self.sharingId}", "sharedFileId": "{self.sharedFileId}","transmitterId": "{self.transmitterId}", "recieverId": "{self.recieverId}", "key": "{self.key}"}}'
    
    def __repr__( self ):
        return f'{{"sharingId": "{self.sharingId}", "sharedFileId": "{self.sharedFileId}","transmitterId": "{self.transmitterId}", "recieverId": "{self.recieverId}", "key": "{self.key}"}}'
    
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
            return Result(200, "Archivo compartido con éxito", True, {"sharedFileId": file.fileId, "transmitterId": file.userId, "recieverId": recieverId, "key": key})
        except:
            return Result(500, "Error en el servidor al compartir fichero", False)