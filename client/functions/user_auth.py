import secrets
from argon2 import PasswordHasher, Type
import requests
import base64
import queue, threading
import re

from functions import otp_things
from functions import debug
from functions.user import User
from functions.rsa import generate_rsa_keys, export_keys, import_public_key, import_private_key
from functions.aes import encrypt_private_key_with_aes, decrypt_private_key_with_aes
from functions.result import Result
from functions.consts import server


def comprobarDatosRegistro(username, email, password, password2):
    error = ''

    caracteres_especiales_permitidos = "!@#$%^&*()\\-_=+<>?[]}{|~"
    caracteres_validos = f"a-zA-Z0-9{re.escape(caracteres_especiales_permitidos)}"
    regex_email = r"^(?=[\w!#$%&'*+/=?^_{|}~.-]{1,64}@)(?=.{1,254}$)(?!.*\.\.)[\w!#$%&'*+/=?^_{|}~-]+(?:\.[\w!#$%&'*+/=?^_{|}~-]+)*@[a-zA-Z0-9-]{1,63}(\.[a-zA-Z0-9-]{1,63}){0,255}$"

    if not all([username, email, password, password2]):
        error = "Por favor, completa todos los campos"   
    elif len(username) < 3 or len(username) > 20:
        error = "Error: El nombre de usuario debe tener entre 3 y 20 caracteres"
    elif not re.match(r'^[a-zA-Z0-9_]+$', username):
        error = "Error: El nombre de usuario solo puede contener letras del alfabeto inglés, números y guiones bajos"
    elif not re.match(regex_email, email):
        error = "Error: El formato del correo electrónico no es válido"
    elif len(password) < 8:
        error = "Error: La contraseña tiene que tener minimo 8 caracteres"
    elif not re.search(r'[a-z]', password):
        error = "Error: La contraseña debe contener al menos una letra minúscula"
    elif not re.search(r'[A-Z]', password):
        error = "Error: La contraseña debe contener al menos una letra mayúscula"
    elif not re.search(r'[0-9]', password):
        error = "Error: La contraseña debe contener al menos un número"
    elif not re.search(r'[!@#$%^&*()\-_=+<>?[\]{}|~]', password):
        error = "Error: La contraseña debe contener al menos un carácter especial de los siguientes: !@#$%^&*()\\-_=+<>?[\\]}{|~"
    elif not re.match(f"^[{caracteres_validos}]+$", password):
        error = "Error: La contraseña contiene caracteres no permitidos: solo se admiten letras del alfabeto inglés, números y carácteres especiales de la siguiente lista: !@#$%^&*()\\-_=+<>?[\\]}{|~"
    elif password2 != password:
        error = "Error: Datos incorrectos: las contraseñas no coinciden"

    return error

def comporbarDatosLogin(email, password):
    error = ''
    regex_email = r"^(?=[\w!#$%&'*+/=?^_{|}~.-]{1,64}@)(?=.{1,254}$)(?!.*\.\.)[\w!#$%&'*+/=?^_{|}~-]+(?:\.[\w!#$%&'*+/=?^_{|}~-]+)*@[a-zA-Z0-9-]{1,63}(\.[a-zA-Z0-9-]{1,63}){0,255}$"


    if not all([email, password]):
        error = "Por favor, completa todos los campos"   
    elif (email == '' or password == ''):
        error = 'Por favor, introduce un email y contraseña'
    elif not re.match(regex_email, email):
        error = "Error: El formato del correo electrónico no es válido"
    
    return error

def pass_management(password, salt) -> str:

    ph = PasswordHasher(
        time_cost=3,          # iterations
        memory_cost=65536,    # KiB (1024 bytes)
        parallelism=4,        # threads
        hash_len=32,          # bytes
        salt_len=16,          # bytes
        encoding='utf-8', 
        type=Type.ID
    )

    resultArgon2id = ph.hash(password, salt=salt)

    parts = resultArgon2id.split('$')
    finalHash = parts[-1] + '=='
    finalHash = base64.b64decode(finalHash)

    derivedPassword = base64.b64encode(finalHash[:16]).decode('utf-8')
    aesKey = finalHash[16:]

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
    

def check2fa(user: User, otp, result_queue) -> User | Result:
    # Llamar a la función login() para realizar un registro
    otp_result = otp_things.check_otp(user.userId, otp)
    if otp_result["code"] == 200:
        privateRSA  = otp_result["body"]["privateRSA"]
        publicRSA   = otp_result["body"]["publicRSA"]
        
        print( debug.printMoment(), "publicRSA: ", publicRSA)
        
        importedPublicKey  = import_public_key(public_key_pem = publicRSA)
        decryptedPrivateKey = decrypt_private_key_with_aes(encrypted_private_key_pem = privateRSA, aes_key = user.aesHash)
        importedPrivateKey = import_private_key(private_key_pem = decryptedPrivateKey)
        
        user.privateRSA = importedPrivateKey
        user.publicRSA = importedPublicKey
        result_queue.put(user)
    
    else:
        result = request_error(otp_result)
        result_queue.put(result)
        return
        

def login(email, password, result_queue) -> User | Result:
    error = comporbarDatosLogin(email, password)

    if ( error ):
        result = Result(400, error, False, error)
        result_queue.put(result)
        return 

    # Obtenemos el salt correspondiente al email
    salt_result = requests.post(server+"/users/getSaltByEmail", json = {
        "email": email
    })

    print("Salt_result: ", salt_result)

    salt_result_json = salt_result.json()
    
    if(str(salt_result_json["code"]) == "200"):

        salt = salt_result_json["body"]["salt"];
        salt = base64.b64decode(salt)
        derivedPassword, aes_key = pass_management(password, salt)

    elif(str(salt_result_json["code"]) == "400"):

        respuesta = 'Email o contraseña incorrectos'
        result = Result(400, respuesta, False, respuesta)
        result_queue.put(result)
        return
    
    else:
  
        result = request_error(salt_result_json)
        result_queue.put(result)
        return

    # Llamar a la función login() para realizar un registro
    login_result = requests.post(server+"/users/login", json = {
        "email": email,
        "password": derivedPassword
    })    
    login_result_json = login_result.json()


    if(str(login_result_json["code"]) == "200"):

        userID      = login_result_json["body"]["userID"]

        user = User( userId = userID, privateRSA = 'tmp', publicRSA = 'tmp', aesHash = aes_key )  
        result_queue.put(user)
        
    else:

        result = request_error(login_result_json)
        result_queue.put(result)
        return
