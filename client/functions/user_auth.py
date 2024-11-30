import json
import secrets
import string
from Crypto.Hash import SHA3_256
from Crypto.Protocol.KDF import PBKDF2
import requests
from pathlib import Path
import os
import base64


from functions.user import User
from functions.rsa import generate_rsa_keys, export_keys, import_public_key, import_private_key
from functions.aes import encrypt_private_key_with_aes, decrypt_private_key_with_aes
from functions.result import Result

global server
server = "http://127.0.0.1:5000"

# Geredor de contraseñas seguras formadas por letras ASCII estándar a-Z, números 0-9 y signos de
# puntuacion !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
def generate_secure_password(length=16):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for i in range(length))

# passphrase = generate_secure_password()
# print(f"Generated passphrase: {passphrase}")

def comprobarDatosRegistro(username, email, password, password2):
    error = ''

    if username is None or email is None or password is None or password2 is None:
        error = "Error: Hay campos vacíos"   
    elif len(password) < 8:
        error = "Error: La contraseña tiene que tener minimo 8 caracteres"
    elif password2 != password:
        error = "Error: Datos incorrectos: las contraseñas no coinciden"

    return error

def register(username, email, password, password2) -> User | Result: 
    # Verificar que las contraseñas coinciden
    error = comprobarDatosRegistro(username, email, password, password2)
    
    if ( error ):
        return Result(400, error, False, error)
    
    # Proteger la contraseña introducida por el usuario
    plain_password = password
    salt = secrets.token_bytes(16)
    derivedPassword, aes_key = pass_management(plain_password, salt)
    salt = base64.b64encode(salt).decode('utf-8')

    # Llamar a la función register() para realizar un registro
    register_result = requests.put(server+"/users/register", json = {
        "user": username,
        "password": derivedPassword,
        "salt": salt,
        "email": email,
        "publicRSA": None,
        "privateRSA": None
    })

    register_result_json = register_result.json()

    if (str(register_result_json["code"]) == "200"):
        # Recogemos el userID
        userID = register_result_json["body"]["userID"]
        # Generar las claves RSA
        privateRSA, publicRSA = generate_rsa_keys()
        # Exportar las claves RSA
        pemPrivateRSA, pemPublicRSA = export_keys(private_key = privateRSA, public_key = publicRSA)
        # Encriptar la RSA privada antes de subirla al servidor
        # encryptedPEMPrivateRSA = encrypt_private_key_with_aes(private_key_pem = pemPrivateRSA, aes_key = aes_key.encode("utf-8"))
        # print("AES KEY: " + aes_key)
        # print("AES KEY ENCODED: " +aes_key.encode("utf-8"))

        encryptedPEMPrivateRSA = encrypt_private_key_with_aes(private_key_pem = pemPrivateRSA, aes_key = aes_key)
        
        # Hacemos la peticion decodificando ambas claves para que la DB pueda interpretarlas (no acepta strings binarios)
        update_result = requests.post(server + "/users/update-keys", json = {
            "userID": userID,
            "privateRSA": encryptedPEMPrivateRSA.decode("utf-8"),
            "publicRSA": pemPublicRSA.decode("utf-8")
        })
        
        update_result_json = update_result.json()
        
        # Comprobamos el resultado de la request
        if (str(update_result_json["code"]) == "200"):
            user = login( email = email, password = plain_password )
            return user
        
        else:
            return Result(
                    update_result_json["code"], 
                    update_result_json["msg"],
                    update_result_json["status"],
                    update_result_json["body"]
                )
    
    else:
        # En caso de que la primera request falle...
        return Result(
            register_result_json["code"], 
            register_result_json["msg"],
            register_result_json["status"],
            register_result_json["body"]
        )
        

def login(email, password) -> User | Result:
    respuesta = ''

    if(email == '' or password == ''):
        respuesta = 'Por favor, introduce un email y contraseña'

    # Se podrian testear expresiones regular
    #     regex = re.compile(r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")

    # def isValid(email):
    #     if re.fullmatch(regex, email):
    #         print("Valid email")
    #     else:
    #         print("Invalid email")
    if "@" not in email:
        respuesta = 'Por favor, introduce un email válido'
    
    # ---------------------------------------------------
    # Hacer peticion si el email existe recuperar el salt
    # ---------------------------------------------------
    salt_result = requests.post(server+"/users/getSaltByEmail", json = {
        "email": email
    })
    
    print("SALT RESULT: ", salt_result)

    salt_result_json = salt_result.json()

    if(str(salt_result_json["code"]) == "200"):
        salt = salt_result_json["body"]["salt"];
        derivedPassword, aes_key = pass_management(password, salt)
    
    print("Salt")
    print(salt)
    print("Derived Password:")
    print(derivedPassword)

    # Llamar a la función login() para realizar un registro
    login_result = requests.post(server+"/users/login", json = {
        "email": email,
        "password": derivedPassword
    })
    
    print("LOGIN RESULT: ", login_result)
    
    login_result_json = login_result.json()
    
    if ( respuesta ):
        return Result(
            400,
            respuesta,
            False,
            respuesta
        )
    
    if(str(login_result_json["code"]) == "200"):
        
        # hacer una peticion que me devuelva la clave privada del usuario
        userID      = login_result_json["body"]["userID"]
        privateRSA  = login_result_json["body"]["privateRSA"]
        publicRSA   = login_result_json["body"]["publicRSA"]
        
        # desencriptar con aes la pass_hash_part2, descifrar y guardar en local
        
        # Las claves no van y no puedo mas :C
        importedPublicKey  = import_public_key(public_key_pem = publicRSA)
        
        decryptedPrivateKey = decrypt_private_key_with_aes(encrypted_private_key_pem = privateRSA, aes_key = aes_key)
        
        importedPrivateKey = import_private_key(private_key_pem = decryptedPrivateKey)
            
        user = User( userId = userID, privateRSA = importedPrivateKey, publicRSA = importedPublicKey, aesHash = aes_key )
        
        return user
    
    else:
        return Result(
            login_result_json["code"],
            login_result_json["msg"],
            login_result_json["status"],
            login_result_json["body"],
        )

        

def pass_management(password, salt) -> str:
    keys = PBKDF2(password, salt, 32, count=100000, hmac_hash_module=SHA3_256)
    
    derivedPassword = base64.b64encode(keys[:16]).decode('utf-8')
    aesKey = keys[16:]
    
    return derivedPassword, aesKey
    
    
# if __name__ == "__main__":
    # login("uncorreo@gamil.com", "12345678")
    # register(email="uncorreo@gamil.com", password="12345678", password2="12345678", username="AAAA" )