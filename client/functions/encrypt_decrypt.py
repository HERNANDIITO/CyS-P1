import os
import requests
from functions.user import User
import functions.aes as aes
import functions.rsa as rsa
import functions.file_requests as file_request

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

    # Obtenemos la clave RSA pública del usuario pasado por parámetro
    rsa_private_key = user.privateRSA
    rsa_public_key = user.publicRSA

    # Ciframos la clave AES128 con la que hemos cifrado el archivo con la clave pública RSA
    file_aes_key_encrypted = rsa.rsa_encrypt(file_aes_key, rsa_public_key)

    # Subimos el archivo al servidor
    user_id = user.userId
    
    # Subimos el archivo
    file_request.upload_file(file_aes_key_encrypted, user_id, b64encoded_encrypted_file, file_type, file_name)

   
# Funcion principal para gestionar el descifrado de archivos multimedia
def decrypt(file_path, user: User, file_name, encrypted_file, file_aes_key_encrypted, file_type):

    # PETICION PARA RECUPERAR EL ARCHIVO DEL SERVIDOR
    # Recuperamos la información almacenada en la base de datos
    #file_name, encrypted_file, file_aes_key_encrypted, file_type = get_encrypted_data_from_db(file_path)

    # Obtenemos la clave RSA privada del usuario
    rsa_private_key = user.privateRSA

    # Desciframos la clave AES128 utilizada para cifrar el archivo con la clave privada RSA
    file_aes_key = rsa.rsa_decrypt(file_aes_key_encrypted, rsa_private_key)

    # Desciframos el archivo con la clave AES128
    decrypted_file = file_name + file_type
    aes.decrypt_file(encrypted_file, decrypted_file, file_aes_key)

    return decrypted_file
