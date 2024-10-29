import json
import secrets
import string
from Crypto.Hash import SHA3_256
import requests
from pathlib import Path
import os

from functions.user import User
from functions.rsa import generate_rsa_keys, export_keys, import_public_key, import_private_key
from functions.aes import encrypt_private_key_with_aes, decrypt_private_key_with_aes


global server
server = "http://127.0.0.1:5000"

# Geredor de contraseñas seguras formadas por letras ASCII estándar a-Z, números 0-9 y signos de
# puntuacion !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
def generate_secure_password(length=16):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for i in range(length))

# passphrase = generate_secure_password()
# print(f"Generated passphrase: {passphrase}")


def register(username, email, password, password2) -> User | None: 
    # Verificar que las contraseñas coinciden
    
    if username is None or email is None or password is None or password2 is None:
        print("Error: Hay campos vacíos")
        return
        
    if len(password) < 8:
        print("Error: La contraseña tiene que tener minimo 8 caracteres")
        return
    
    if password2 != password:
        print("Error: Datos incorrectos: las contraseñas no coinciden")
        return
    
    # Encriptar la contraseña
    plain_password = password
    password, aes_key = hash_management(password)
    
    
    # Llamar a la función register() para realizar un registro
    register_result = requests.put(server+"/users/register", json = {
        "user": username,
        "password": password,
        "email": email,
        "publicRSA": None,
        "privateRSA": None
    })

    register_result_json = json.loads(register_result.text)

    if (str(register_result_json["code"]) == "200"):
        # Recogemos el userID
        userID = register_result_json["body"]["userID"]
        # Generar las claves RSA
        privateRSA, publicRSA = generate_rsa_keys()
        # Exportar las claves RSA
        pemPrivateRSA, pemPublicRSA = export_keys(private_key = privateRSA, public_key = publicRSA)
        # Encriptar la RSA privada antes de subirla al servidor
        encryptedPEMPrivateRSA = encrypt_private_key_with_aes(private_key_pem = pemPrivateRSA, aes_key = aes_key.encode("utf-8"))
        
        # Hacemos la peticion decodificando ambas claves para que la DB pueda interpretarlas (no acepta strings binarios)
        update_result = requests.post(server + "/users/update-keys", json = {
            "userID": userID,
            "privateRSA": encryptedPEMPrivateRSA.decode("utf-8"),
            "publicRSA": pemPublicRSA.decode("utf-8")
        })
        
        update_result_json = json.loads(update_result.text)
        
        # Comprobamos el resultado de la request
        if (str(update_result_json["code"]) == "200"):
            user = login( email = email, password = plain_password )
            return user
    
    else:
        # En caso de que la primera request falle...
        return None
        

def login(email, password) -> User | None:
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
        
    password, aes_key = hash_management(password)
    
    # Llamar a la función login() para realizar un registro
    login_result = requests.post(server+"/users/login", json = {
        "email": email,
        "password": password
    })
    
    login_result_json = json.loads(login_result.text)
    
    print("PRE 200!")
    print( "code", json.loads(login_result.text) )
    print( "email", email )
    print( "password", password )
    if(str(json.loads(login_result.text)["code"]) == "200"):
        
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
        return None

        

def hash_management(password) -> str:
    pass_hash = SHA3_256.new()
    pass_hash.update(bytes(password, encoding="utf-8"))
    
    pass_hash_hex = pass_hash.hexdigest()

    pass_hash_part1 = pass_hash_hex[:int(len(pass_hash_hex)/2)] # Devolvemos la parte a la BD
    pass_hash_part2 = pass_hash_hex[-int(len(pass_hash_hex)/2):] # Guardamos en local
    
    return pass_hash_part1, pass_hash_part2
    
    
if __name__ == "__main__":
    login("uncorreo@gamil.com", "12345678")
    register(email="uncorreo@gamil.com", password="12345678", password2="12345678", username="AAAA" )