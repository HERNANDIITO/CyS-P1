from functions import database as db 

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
