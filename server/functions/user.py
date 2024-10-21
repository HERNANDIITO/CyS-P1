from typing import List
from functions import database as db 
from functions.result import Result
from google.oauth2 import id_token
from google.auth.transport import requests

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
    def register( self, user: str, password: str, email: str, publicRSA: str, privateRSA: str  ) -> Result:

        # Comprobar que tenemos todos los parametros necesarios
        # En caso de no tenerlo montamos un objeto tipo result para devolverlo
        if user == None or password == None or email == None:
            # Esta funcion crea un objeto tipo result con los parametros indicados
            # en este ejemplo concreto he puesto lo que significan los parametros, pero mas adelante se omitira
            return Result( code = 400, msg = "Mala solicitud: faltan parámetros", status = False)
        
        # Intentamos recoger un usuario con el mismo email que acabamos de recibir
        userData = db.get_data( "users", { "email": email })

        # Si hay algo en la variable, significa que ya hay un usuario registrado bajo ese email
        # No permitimos otro
        # if userData:
        #     return Result(400, "Mala solicitud: email en uso", False)

        # Intentamos introducir el usuario nuevo en la base de datos 
        try:
            db.insert_data("users", {
                "userId": None,
                "user": user, 
                "password": password,
                "salt": None,
                "publicRSA": publicRSA,
                "privateRSA": privateRSA,
                "email": email
            })
            userID = db.get_data( "users", { "email": email } )[0]
        # Si algo falla devolvemos un result informando
        except:
            return Result(500, "Algo ha ido mal", False)

        # Si el código ha llegado hasta aquí significa que todo ha ido bien, por lo que devolvemos un mensaje positivo
        return Result(200, "Usuario registrado con éxito", True, {"userID": userID})
    
    @classmethod
    def login(self, email: str, password: str) -> Result:

        # Intentamos recoger un usuario con el mismo email que acabamos de recibir
        userData = db.get_data( "users", { "email": email })

        # Si no hay nada en la variable, significa que el usuario no existe
        # No permitimos otro
        if not userData:
            return Result(400, "Mala solicitud: el usuario no existe", False)

        if str(password) != str(userData[2]):
            return Result(400, "Mala solicitud: contraseña equivocada", False)
        
        user = User(userData[0])
        
        # Añadimos el id de usuario a la solicitud para recogerla desde desde el cliente
        # y poder utilizarla en los siguientes servicios
        return Result(200, "Sesión iniciada con éxito", True, {"userID": user.userId, "privateRSA": user.privateRSA, "publicRSA": user.publicRSA})

    @classmethod
    def getAllUsers( self ) -> List['User']:
        userRawList = db.get_all_data("users")
        userList = []

        for user in userRawList:
            userList.append( User(user[0]) )

        return userList
    
    def modifyKeys( self, privateRSA: str, publicRSA: str ):
        try: 
            db.update_data( "users", {
                "privateRSA": privateRSA,
                "publicRSA": publicRSA,
                "userID": self.userId
            }, { "userId": self.userId })
            return Result(body= None, code="200", msg= "Claves modificadas con éxito", status=True)
        except:
            return Result(body= None, code="500", msg= "Error del servidor, inténtalo más tarde", status=False)
        

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
    
    @classmethod
    def loginGoogle(sel, token: str) -> Result:
        try:
            # Comprueba que el token es valido
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), '930275995654-845nchda7mj5aqm2dit8c7kvv8h92ag4.apps.googleusercontent.com')

            # ID token is valid. Get the user's email from the decoded token.
            user_email = idinfo['email']
            
            # Intentamos recoger un usuario con el mismo email que acabamos de recibir
            userData = db.get_data( "users", { "email": user_email })

            # Si no hay nada en la variable, significa que el usuario no existe
            # No permitimos otro
            if not userData:
                return Result(400, "Mala solicitud: el usuario no existe", False)
            
            # Añadimos el id de usuario a la solicitud para recogerla desde desde el cliente
            # y poder utilizarla en los siguientes servicios
            return Result(200, "Sesión iniciada con éxito", True, {"userID": userData[0], "privateRSA": userData[5]})
        
        except ValueError:
            # Invalid token
            return Result(400, "Mala solicitud: el id_token de Google no es válido", False)