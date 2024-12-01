import string
import secrets
from Crypto.Hash import SHA3_256
from Crypto.Protocol.KDF import PBKDF2
import requests
import base64
import queue, threading

from functions import debug
from functions.user import User
from functions.rsa import generate_rsa_keys, export_keys, import_public_key, import_private_key
from functions.aes import encrypt_private_key_with_aes, decrypt_private_key_with_aes
from functions.result import Result


global server
server = "http://127.0.0.1:5000"


def comprobarDatosRegistro(username, email, password, password2):
    error = ''

    if username is None or email is None or password is None or password2 is None:
        error = "Error: Hay campos vacíos"   
    elif len(password) < 8:
        error = "Error: La contraseña tiene que tener minimo 8 caracteres"
    elif password2 != password:
        error = "Error: Datos incorrectos: las contraseñas no coinciden"

    return error

def comporbarDatosLogin(email, password):
    error = ''

    if (email == '' or password == ''):
        error = 'Por favor, introduce un email y contraseña'
    elif "@" not in email:
        error = 'Por favor, introduce un email válido'
    
    return error


def pass_management(password, salt) -> str:
    keys = PBKDF2(password, salt, 32, count=100000, hmac_hash_module=SHA3_256)
    
    derivedPassword = base64.b64encode(keys[:16]).decode('utf-8')
    aesKey = keys[16:]

    return derivedPassword, aesKey

def request_error(response):
    return Result(
        response["code"], 
        response["msg"],
        response["status"],
        response["body"]
    )
    

def register(username, email, password, password2) -> User | Result: 
    error = comprobarDatosRegistro(username, email, password, password2)
    
    if ( error ):
        return Result(400, error, False, error)
    
    # Generar salt para proteger la contraseña introducida por el usuario con pbkdf2
    salt = secrets.token_bytes(16)
    derivedPassword, aes_key = pass_management(password, salt)
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
        # Encriptar la clave RSA privada antes de subirla al servidor
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
            result_queue = queue.Queue()
            hilo = threading.Thread(target=login, args=(email, password, result_queue))
            hilo.daemon = True  # Asegura que el hilo se cierre al cerrar la app
            hilo.start()
            hilo.join()
            user = result_queue.get()
            return user
        
        else:
            return request_error(update_result_json)
    else:
        # En caso de que la primera request de registro de nuevo usuario falle...
        return request_error(register_result_json)
        

def login(email, password, result_queue) -> User | Result:
    error = comporbarDatosLogin(email, password)

    if ( error ):
        return Result(400, error, False, error)

    # Obtenemos el salt correspondiente al email
    salt_result = requests.post(server+"/users/getSaltByEmail", json = {
        "email": email
    })

    salt_result_json = salt_result.json()

    if(str(salt_result_json["code"]) == "200"):
        salt = salt_result_json["body"]["salt"];
        salt = base64.b64decode(salt)
        derivedPassword, aes_key = pass_management(password, salt)
    
        # Llamar a la función login() para realizar un registro
        login_result = requests.post(server+"/users/login", json = {
            "email": email,
            "password": derivedPassword
        })
        
        login_result_json = login_result.json()
        
        if ( error ):
            return Result(400, error, False, error)
        
        if(str(login_result_json["code"]) == "200"): 
            userID      = login_result_json["body"]["userID"]
            privateRSA  = login_result_json["body"]["privateRSA"]
            publicRSA   = login_result_json["body"]["publicRSA"]

            importedPublicKey  = import_public_key(public_key_pem = publicRSA)
            decryptedPrivateKey = decrypt_private_key_with_aes(encrypted_private_key_pem = privateRSA, aes_key = aes_key)
            importedPrivateKey = import_private_key(private_key_pem = decryptedPrivateKey)

            user = User( userId = userID, privateRSA = importedPrivateKey, publicRSA = importedPublicKey, aesHash = aes_key )
            
            result_queue.put(user)
        
        else:
            result = request_error(login_result_json)
            result_queue.put(result)
    else:
        result = request_error(salt_result_json)
        result_queue.put(result)


        
