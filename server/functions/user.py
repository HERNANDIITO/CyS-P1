from typing import List
from functions import database as db 

class User:
    def __init__( self, userId: str ):
        userData = db.get_data( "users", { "userId": userId })
        
        self.userId     = userData[0]
        self.user       = userData[1]
        self.password   = userData[2]
        self.salt       = userData[3]
        self.publicRSA  = userData[4]
        self.privateRSA = userData[5]
        self.email      = userData[6]
    
    def __str__( self ):
        return f'{{"userId": "{self.userId}","user": "{self.user}", "password": "{self.password}","salt": "{self.salt}","publicRSA": "{self.publicRSA}","privateRSA": "{self.privateRSA}","email": "{self.email}"}}'
    
    def __repr__( self ):
        return f'{{"userId": "{self.userId}","user": "{self.user}", "password": "{self.password}","salt": "{self.salt}","publicRSA": "{self.publicRSA}","privateRSA": "{self.privateRSA}","email": "{self.email}"}}'

    @classmethod
    def createUser( self, user: str, password: str, salt: str, publicRSA: str, privateRSA: str, email: str ) -> None:
        db.insert_data("users", {
            "userId": None,
            "user": user, 
            "password": password,
            "salt": salt,
            "publicRSA": publicRSA,
            "privateRSA": privateRSA,
            "email": email
        })


    @classmethod
    def getAllUsers( self ) -> List['User']:
        userRawList = db.get_all_data("users")
        userList = []

        for user in userRawList:
            userList.append( User(user[0]) )

        return userList

        
    def modifyUser( self, userId: str, user: str | None = None, password: str | None = None ) -> "User":
        toModify = User(userId)
        if ( user ):
            toModify.user = user
        
        if ( password ):
            toModify.password = password
        
        db.update_data("users", {
            "user": toModify.user,
            "password": toModify.password,
        }, { "userId": userId })

        return toModify

    def getFiles( self ) -> List[str]:
        return db.get_data( "files", { "user": self.userId } )