from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

# Función para cifrar el contenido de un archivo
def encrypt_file(input_file, output_file, key):
    # Lectura del archivo original
    with open(input_file, 'rb') as f:
        data = f.read()
    
    # Padding para ajustar el tamaño del bloque de 16 bytes
    padded_data = pad(data, AES.block_size)
    
    # Creación del objeto AES en modo ECB
    cipher = AES.new(key, AES.MODE_ECB)
    
    # Cifrado de los datos
    encrypted_data = cipher.encrypt(padded_data)
    
    # Guardamos los datos cifrados en un archivo de salida
    with open(output_file, 'wb') as f:
        f.write(encrypted_data)

# Función para descifrar un archivo
def decrypt_file(input_file, output_file, key):
    # Lectura del archivo cifrado
    with open(input_file, 'rb') as f:
        encrypted_data = f.read()
    
    # Creación del objeto AES en modo ECB
    cipher = AES.new(key, AES.MODE_ECB)
    
    # Descifrado de los datos
    decrypted_data = cipher.decrypt(encrypted_data)
    
    # Quitamos el padding
    original_data = unpad(decrypted_data, AES.block_size)
    
    # Guardamos los datos descifrados en un archivo de salida
    with open(output_file, 'wb') as f:
        f.write(original_data)

# Función principal para ejecutar el cifrado y descifrado
if __name__ == "__main__":
    # Clave de 16 bytes (128 bits) - Debe ser secreta
    key = b'ThisIsA16ByteKey'  # Asegúrate de tener una clave de 16 bytes para AES-128
    
    # Archivos de entrada y salida
    input_file = 'patata.txt'
    encrypted_file = 'archivo_encriptado.bin'
    decrypted_file = 'archivo_descifrado.txt'
    
    # Cifrar el archivo
    encrypt_file(input_file, encrypted_file, key)
    print(f"Archivo {input_file} cifrado en {encrypted_file}.")
    
    # Descifrar el archivo
    decrypt_file(encrypted_file, decrypted_file, key)
    print(f"Archivo {encrypted_file} descifrado en {decrypted_file}.")
