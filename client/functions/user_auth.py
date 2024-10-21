import json
import secrets
import string
from Crypto.Hash import SHA3_256
import requests

from functions.rsa import generate_rsa_keys, export_keys
from functions.aes import encrypt_private_key_with_aes

global server
server = "http://127.0.0.1:5000"

# Geredor de contraseñas seguras formadas por letras ASCII estándar a-Z, números 0-9 y signos de
# puntuacion !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
def generate_secure_password(length=16):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for i in range(length))

passphrase = generate_secure_password()
print(f"Generated passphrase: {passphrase}")


def register(username, email, password, password2): 
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
    password, aes_key = hash_management(password)
    
    
    # Llamar a la función register() para realizar un registro
    register_result = requests.put(server+"/users/register", json = {
        "user": username,
        "password": password,
        "email": email,
        "publicRSA": None,
        "privateRSA": None
    })

    
    body = json.loads(register_result.text)["body"].replace("'", '"')
    userID = json.loads(body)["userID"]
    
    if (json.loads(register_result.text)["code"] == "200"):
        # Generar las claves RSA
        privateRSA, publicRSA = generate_rsa_keys()
        pemPrivateRSA, pemPublicRSA = export_keys(private_key = privateRSA, public_key = publicRSA)
        encryptedPEMPrivateRSA = encrypt_private_key_with_aes(private_key_pem = pemPrivateRSA, aes_key = aes_key)
        
        update_result = requests.post(server + "/users/update-keys", json = {
            "userID": userID,
            "privateRSA": encryptedPEMPrivateRSA,
            "publicRSA": pemPublicRSA
        })
        
        
        
        


def login(email, password) -> str:
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
    r = requests.put(server+"/users/login", json = {
        "email": email,
        "password": password
    })
    
    # if(json.loads(r.text)["code"] == "200"):
        # hacer una peticion que me devuelva la clave privada del usuario
        # desencriptar con aes la pass_hash_part2, descifrar y guardar en local
        

def hash_management(password):
    pass_hash = SHA3_256.new()
    pass_hash.update(bytes(password, encoding="utf-8"))
    
    pass_hash_hex = pass_hash.hexdigest()

    pass_hash_part1 = pass_hash_hex[:int(len(pass_hash_hex)/2)] # Devolvemos la parte a la BD
    pass_hash_part2 = pass_hash_hex[-int(len(pass_hash_hex)/2):] # Guardamos en local
    
    return pass_hash_part1, pass_hash_part2
    
    
if __name__ == "__main__":
    login("uncorreo@gamil.com", "12345678")
    register(email="uncorreo@gamil.com", password="12345678", password2="12345678", username="AAAA" )