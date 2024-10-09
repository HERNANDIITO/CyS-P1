
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import secrets

    #Genera una clave AES de 16 bytes (128 bits).
def generate_aes_key():
    return secrets.token_bytes(16)

    #Cifra el contenido de un archivo utilizando AES (en modo ECB por ahora, mas adelante en CTR).
def encrypt_file(input_file, output_file, aes_key):
    with open(input_file, 'rb') as f:
        data = f.read()

    padded_data = pad(data, AES.block_size)
    cipher = AES.new(aes_key, AES.MODE_ECB)
    encrypted_data = cipher.encrypt(padded_data)

    with open(output_file, 'wb') as f:
        f.write(encrypted_data)

    #Descifra un archivo utilizando AES en modo ECB.
def decrypt_file(input_file, output_file, aes_key):
    with open(input_file, 'rb') as f:
        encrypted_data = f.read()

    cipher = AES.new(aes_key, AES.MODE_ECB)
    decrypted_data = cipher.decrypt(encrypted_data)
    original_data = unpad(decrypted_data, AES.block_size)

    with open(output_file, 'wb') as f:
        f.write(original_data)

    #Cifra una clave privada RSA utilizando AES128.
def encrypt_private_key_with_aes(private_key_pem, aes_key):
    padded_private_key = pad(private_key_pem, AES.block_size)
    cipher = AES.new(aes_key, AES.MODE_ECB)
    encrypted_private_key = cipher.encrypt(padded_private_key)
    return encrypted_private_key

    #Descifra una clave privada RSA utilizando AES128.
def decrypt_private_key_with_aes(encrypted_private_key, aes_key):
    cipher = AES.new(aes_key, AES.MODE_ECB)
    decrypted_private_key_pem = cipher.decrypt(encrypted_private_key)
    private_key_pem = unpad(decrypted_private_key_pem, AES.block_size)
    return private_key_pem
