# main.py

from aes import generate_aes_key, encrypt_file, decrypt_file, encrypt_private_key_with_aes, decrypt_private_key_with_aes
from rsa import generate_rsa_keys, rsa_encrypt, rsa_decrypt, export_keys, import_keys

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

    # Exportar las claves a archivos PEM
    export_keys(private_key, public_key)

if __name__ == "__main__":
    encrypt_decrypt()
