import os
from aes import *
from rsa import *


def get_file_name_and_type(file_path):
    file_name = os.path.basename(file_path)
    file = os.path.splitext(file_name)
    return file[0], file[1]

# FUNCIONES DE CONTACTO CON LA BD----------------------------------------------------------------------------------------------------------------


def store_encrypted_data_in_db(file_name, encrypted_file, file_aes_key_encrypted, rsa_public_key_pem, encrypted_rsa_private_key_pem, rsa_aes_key, file_type):
    # obtener userId, date con SYSDATE?, fileId creo que no hace falta
    file_data {
        fileName: file_name,
        encryptedFile: encrypted_file,
        AESKey: file_aes_key_encrypted,
        publicRSA:  rsa_public_key_pem,
        privateRSA: encrypted_rsa_private_key_pem,
        rsaAESKey: rsa_aes_key,  # deberiamos de protegerla de algun modo
        fileType: file_type
    }

    save_new_file(file_data)


def get_encrypted_data_from_db(file_path):
    


# FUNCIONES DE ENCRIPTADO Y DESENCRIPTADO--------------------------------------------------------------------------------------------------------

# Funcion principal para gestionar el cifrado de archivos multimedia
def encrypt(file_path): 
    # Generamos una clave AES128 para cifrar el archivo
    file_aes_key = generate_aes_key()

    # Obtenemos el nombre y extension del fichero
    file_name, file_type = get_file_name_and_type(file_path)

    # Creamos el archivo de salida, resultado cifrado
    encrypted_file = "file_encrypted.txt"

    # Ciframos el archivo con AES128
    encrypt_file(file_path, encrypted_file, file_aes_key)

    # Generamos una pareja de claves pública-privada RSA 2048 bits
    rsa_private_key, rsa_public_key = generate_rsa_keys()

    # Ciframos la clave AES128 con la que hemos cifrado el archivo con la clave pública RSA
    file_aes_key_encrypted = rsa_encrypt(file_aes_key, rsa_public_key)

    # Exportamos las claves RSA a formato PEM
    rsa_private_key_pem, rsa_public_key_pem = export_keys(rsa_private_key, rsa_public_key)

    # Protegemos la clave privada RSA con AES128
    rsa_aes_key = generate_aes_key()
    encrypted_rsa_private_key_pem = encrypt_private_key_with_aes(rsa_private_key_pem, rsa_aes_key)

    # Almacenamos la informacion en la base de datos
    # store_encrypted_data_in_db(file_name, encrypted_file, file_aes_key_encrypted, rsa_public_key_pem, encrypted_rsa_private_key_pem, rsa_aes_key, file_type)


# Funcion principal para gestionar el descifrado de archivos multimedia
def decrypt(file_path):
    # Recuperamos la información almacenada en la base de datos
    file_name, encrypted_file, file_aes_key_encrypted, rsa_public_key_pem, encrypted_rsa_private_key_pem, rsa_aes_key, file_type = get_encrypted_data_from_db(file_path)

    # Desciframos la clave privada RSA con la clave AES128
    rsa_private_key_pem = decrypt_private_key_with_aes(encrypted_rsa_private_key_pem, rsa_aes_key)

    # Convertimos la clave privada RSA desde el formato PEM
    rsa_private_key = import_private_key(rsa_private_key_pem)

    # Desciframos la clave AES128 utilizada para cifrar el archivo con la clave privada RSA
    file_aes_key = rsa_decrypt(file_aes_key_encrypted, rsa_private_key)

    # Desciframos el archivo con la clave AES128
    decrypted_file = file_name + file_type
    decrypt_file(encrypted_file, decrypted_file, file_aes_key)

    # return decrypted_file

    # print(f"Archivo descifrado correctamente y guardado como {decrypted_file}")
    
# main para hacer pruebas
if __name__ == "__main__":
    encrypt(r"C:\Users\Laura\Desktop\Captura de pantalla 2024-10-10 172227.png")
