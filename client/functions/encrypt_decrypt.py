
import os
from aes import *
from rsa import *

def encrypt_decrypt():
    # Generar claves RSA
    private_key, public_key = generate_rsa_keys()

    # Generar una clave AES de 16 bytes
    aes_key = generate_aes_key()

    #(aqui almaceno clave en la bd)

    # Cifrar la clave privada con AES128
    private_key_pem = private_key.export_key()
    encrypted_private_key = encrypt_private_key_with_aes(private_key_pem, aes_key)
    print("Clave privada cifrada correctamente.")

    # Descifrar la clave privada con AES128
    decrypted_private_key_pem = decrypt_private_key_with_aes(encrypted_private_key, aes_key)
    print("Clave privada descifrada correctamente.")

    # Verificar que la clave privada descifrada coincida con la original
    if private_key_pem == decrypted_private_key_pem:
        print("La clave privada descifrada coincide con la original. ¡Cifrado y descifrado correctos!")
    else:
        print("Error: La clave privada descifrada no coincide con la original.")

    # Exportar las claves RSA a archivos PEM
    export_keys(private_key, public_key)


def get_file_name_and_type(file_path):
    file_name = os.path.basename(file_path)
    file = os.path.splitext(file_name)
    return file[0], file[1]

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
    store_encrypted_data_in_db(file_name, encrypted_file, file_aes_key_encrypted, rsa_public_key_pem, encrypted_rsa_private_key_pem, rsa_aes_key, file_type)



def decrypt():
    











if __name__ == "__main__":
    encrypt_decrypt()
    encrypt(r"C:\Users\Laura\Desktop\Captura de pantalla 2024-10-10 172227.png")
