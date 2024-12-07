from typing import List
from functions import database as db 
from functions.result import Result
from functions.otp_utils import *

class User:
    def __init__( self, userId: str = None, email: str = None ):
        if ( userId ):
            userData = db.get_data( "users", { "userId": userId })
        elif ( email ):
            userData = db.get_data( "users", { "email": email })
            
        try:
            self.userId     = userData[0]
            self.user       = userData[1]
            self.password   = userData[2]
            self.salt       = userData[3]
            self.publicRSA  = userData[4]
            self.privateRSA = userData[5]
            self.email      = userData[6]
            self.otpSecret  = userData[7] # Esto no sale del servidor
        except:
            self.userId = -1
    
    def __str__( self ):
        return f'{{"userId": "{self.userId}","user": "{self.user}", "password": "{self.password}","salt": "{self.salt}","publicRSA": "{self.publicRSA}","privateRSA": "{self.privateRSA}","email": "{self.email}", "otpSecret": "{self.otpSecret}"}}'
    
    def __repr__( self ):
        return f'{{"userId": "{self.userId}","user": "{self.user}", "password": "{self.password}","salt": "{self.salt}","publicRSA": "{self.publicRSA}","privateRSA": "{self.privateRSA}","email": "{self.email}", "otpSecret": "{self.otpSecret}"}}'

    @classmethod
    def register( self, user: str, password: str, email: str, publicRSA: str, privateRSA: str, salt: str  ) -> Result:

        # Comprobar que tenemos todos los parametros necesarios
        # En caso de no tenerlo montamos un objeto tipo result para devolverlo
        if user == None or password == None or email == None:
            # Esta funcion crea un objeto tipo result con los parametros indicados
            return Result( code = 400, msg = "Mala solicitud: faltan parámetros", status = False)
        
        # Intentamos recoger un usuario con el mismo email que acabamos de recibir
        userData = db.get_data( "users", { "email": email })

        # Si hay algo en la variable, significa que ya hay un usuario registrado bajo ese email
        # No permitimos otro
        if userData:
            return Result(400, "Mala solicitud: email en uso", False)

        # Intentamos introducir el usuario nuevo en la base de datos 
        try:
            codigo_otp = generate_secret_key()
            db.insert_data("users", {
                "userId": None,
                "user": user, 
                "password": password,
                "salt": salt,
                "publicRSA": publicRSA,
                "privateRSA": privateRSA,
                "email": email,
                "otpSecret": codigo_otp
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
        user = User(email=email)

        # Si no hay nada en la variable, significa que el usuario no existe
        # No permitimos otro
        if not user:
            return Result(400, "Mala solicitud: email o contraseña equivocados", False)

        if str(password) != str(user.password):
            return Result(400, "Mala solicitud: email o contraseña equivocados", False)

        # Añadimos el id de usuario a la solicitud para recogerla desde desde el cliente
        # y poder utilizarla en los siguientes servicios
        return Result(200, "Sesión iniciada con éxito", True, {"userID": user.userId})

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
    
    def getSalt(self):
        if ( self.userId == -1 ):
            return Result(400, "El usuario no existe", False, None)
        
        return Result(200, "Salt enviada con éxito", True, {"salt": self.salt})

    def getID(self):
        if ( self.userId == -1 ):
            return Result(400, "El usuario no existe", False, None)
            
        return Result(200, "ID enviada con exito", True, {"userID": self.userId, "publicRSA": self.publicRSA})

    def getPublicRsa(self) -> Result:
        return Result(200, "Clave RSA pública obtenida con éxito", True, {"publicRSA": self.publicRSA})

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

    def getFiles( self ) -> Result:
        result = db.get_file_data_map( "files", { "userId": self.userId } )
        
        if (result != None):
            return Result(200, "Archivos obtenidos con éxito", True, {"files": result})
        
        return Result(404, "El usuario no tiene ficheros", False, {})

    
    def getSharedFilesOfUser(self) -> Result:
        result = db.get_shared_file_data_map( "files", { "transmitterId": self.userId } )
    
        if (result != None):
            return Result(200, "Archivos compartidos por usuario obtenidos con éxito", True, {"files": result})
        
        return Result(404, "El usuario no ha compartido ficheros", False, {})
    
    def getSharedFilesToUser(self) -> Result:
        result = db.get_shared_file_data_map( "files", { "recieverId": self.userId } )
  
        if (result != None):
            return Result(200, "Archivos compartidos al usuario obtenidos con éxito", True, {"files": result})
        return Result(404, "No hay archivos compartidos a este usuario", False, {})

    def changeData(self, user: str, email: str) -> Result:
        try:
            db.update_data( "users", {
                "user": user,
                "email": email,
            }, { "userId": self.userId })
            self.user = user
            self.email = email
            return Result(200, "Datos del usuario modificados con éxito", True, {"userId": self.userId, "user": self.user, "email": self.email, "publicRSA": self.publicRSA, "privateRSA": self.privateRSA, "password": self.password, "salt": self.salt})
        except:
            return Result(500, "Error del servidor al cambiar datos del usuario", False)
        
    def getOtpUrl(self) -> Result:
        url = generate_url(self.otpSecret, self.email)
        return Result(200, "URL de OTP generada con éxito", True, {"url": url})
    
    def checkOtpCode(self, code: str) -> Result:
        if (verify_otp(self.otpSecret, code)):
            return Result(200, "Código OTP correcto", True, {"privateRSA": self.privateRSA, "publicRSA": self.publicRSA})
        return Result(400, "Mala solicitud: código OTP incorrecto", False)