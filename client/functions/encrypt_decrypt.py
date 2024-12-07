import os
from functions.result import Result
from functions.user import User
import functions.aes as aes
import functions.rsa as rsa
import functions.file_requests as file_request

def get_file_name_and_type(file_path):
    try:
        file_name = os.path.basename(file_path)
        file = os.path.splitext(file_name)
        return file[0], file[1]
    except FileNotFoundError:
        print("Error: No se encontró el archivo especificado.")

# FUNCIONES DE CIFRADO Y DESCIFRADO--------------------------------------------------------------------------------------------------------

# Funcion principal para gestionar el cifrado de archivos multimedia
def encrypt(file_path, user): 
    # Generamos una clave AES128 para cifrar el archivo
    file_aes_key = aes.generate_aes_key()

    # Obtenemos el nombre y extension del fichero
    file_name, file_type = get_file_name_and_type(file_path)

    # Creamos el archivo de salida, resultado cifrado
    encrypted_file = "file_encrypted.txt"
    b64encoded_encrypted_file = "b64encoded_encrypted_file.txt"

    # Ciframos el archivo con AES128
    aes.encrypt_file(file_path, encrypted_file, b64encoded_encrypted_file, file_aes_key)

    # Obtenemos las claves RSA pública y privada del usuario pasado por parámetro
    rsa_private_key = user.privateRSA
    rsa_public_key = user.publicRSA

    # Ciframos la clave AES128 con la que hemos cifrado el archivo con la clave pública RSA
    file_aes_key_encrypted = rsa.rsa_encrypt(file_aes_key, rsa_public_key)

    # Firmamos el archivo
    fileToEncrypt = open(file_path, 'rb').read()
    signature = rsa.rsa_sign(fileToEncrypt, rsa_private_key)

    # Subimos el archivo al servidor
    user_id = user.userId
    
    # Subimos el archivo
    result = file_request.upload_file(file_aes_key_encrypted, user_id, b64encoded_encrypted_file, file_type, file_name, signature)
    
    if ( type(result) is Result ):
        return result


# Funcion principal para gestionar el descifrado de archivos multimedia
def decrypt(user: User, file_name, file_aes_key_encrypted, signatory_public_key, signature):
    # Obtenemos la clave RSA privada del usuario
    rsa_private_key = user.privateRSA

    # Desciframos la clave AES128 utilizada para cifrar el archivo con la clave privada RSA
    file_aes_key = rsa.rsa_decrypt(file_aes_key_encrypted, rsa_private_key)

    # Desciframos el archivo con la clave AES128
    aes.decrypt_file(file_name, file_name, file_aes_key)
    
    decrypted_file = open(file_name, 'rb').read()

    autenticity = rsa.rsa_check_sign(decrypted_file, signatory_public_key, signature)
    
    return autenticity

    



