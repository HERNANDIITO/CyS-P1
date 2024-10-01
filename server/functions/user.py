from functions import database as db 

class User:
    def __init__(self, userId: str):
        userData = db.get_data("users", {"userId": userId})
        
        self.userId   = userData[0]
        self.user     = userData[1]
        self.password = userData[2]

    @classmethod
    def createUser(self, userId: str, username: str, password: str):
        db.insert_data("users", {
            "userId": userId,
            "user": username, 
            "password": password
        })

        user = User(userId)

        return user

