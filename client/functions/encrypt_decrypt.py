import os
import requests
from functions.result import Result
from functions.user import User
import functions.aes as aes
import functions.rsa as rsa
import functions.file_requests as file_request
from Crypto.Hash import SHA3_256

global server
server = "http://127.0.0.1:5000"

def get_file_name_and_type(file_path):
    try:
        file_name = os.path.basename(file_path)
        file = os.path.splitext(file_name)
        return file[0], file[1]
    except FileNotFoundError:
        print("Error: No se encontró el archivo especificado.")

# FUNCIONES DE CONTACTO CON LA BD----------------------------------------------------------------------------------------------------------------


# def store_encrypted_data_in_db(file_name, encrypted_file, file_aes_key_encrypted, rsa_public_key_pem, encrypted_rsa_private_key_pem, rsa_aes_key, file_type):
#     # obtener userId, date con SYSDATE?, fileId creo que no hace falta
#     file_data = {
#         'fileName': file_name,
#         'encryptedFile': encrypted_file,
#         'AESKey': file_aes_key_encrypted,
#         'publicRSA':  rsa_public_key_pem,
#         'privateRSA': encrypted_rsa_private_key_pem,
#         'rsaAESKey': rsa_aes_key,  # deberiamos de protegerla de algun modo
#         'fileType': file_type
#     }

#     save_new_file(file_data)


# def get_encrypted_data_from_db(file_path):
    


# FUNCIONES DE ENCRIPTADO Y DESENCRIPTADO--------------------------------------------------------------------------------------------------------

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
    signature = rsa.rsa_sign(file_path, rsa_private_key)

    # Subimos el archivo al servidor
    user_id = user.userId
    
    # Subimos el archivo
    result = file_request.upload_file(file_aes_key_encrypted, user_id, b64encoded_encrypted_file, file_type, file_name, signature)
    
    if ( type(result) is Result ):
        return result


# Funcion principal para gestionar el descifrado de archivos multimedia
def decrypt(user: User, file_name, encrypted_file, file_aes_key_encrypted, file_type, signatory_public_key, signature):

    # PETICION PARA RECUPERAR EL ARCHIVO DEL SERVIDOR
    # Recuperamos la información almacenada en la base de datos
    #file_name, encrypted_file, file_aes_key_encrypted, file_type = get_encrypted_data_from_db(file_path)

    # Obtenemos la clave RSA privada del usuario
    rsa_private_key = user.privateRSA

    # Desciframos la clave AES128 utilizada para cifrar el archivo con la clave privada RSA
    file_aes_key = rsa.rsa_decrypt(file_aes_key_encrypted, rsa_private_key)

    # Desciframos el archivo con la clave AES128
    print(encrypted_file)
    aes.decrypt_file(file_name, file_name, file_aes_key)

    autenticity = rsa.rsa_check_sign(file_name, signatory_public_key, signature)
    
    if(autenticity):
        return decrypted_file
    else:
        return "El archivo no es válido"

    



