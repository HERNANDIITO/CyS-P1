# Este codigo contiene las siguientes funciones:
# - cifrar archivo con aes128
# - descifrar archivo con aes128
# - generar clave aleatoria 16 bytes
# - cifrar la clave AES128 con RSA
# - cifrar la clave RSA con AES128

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
    key16 = os.urandom(16)  # Genera una clave aleatoria

    # ...
    # (AQUI SE ALMACENA LA CLAVE (key16) EN LA BD)
    # ...


    # Mostrar la clave generada
    # print(f"Clave generada: {key.hex()}")
    
    # Archivos de entrada y salida
    input_file = 'mensaje_ejemplo.txt'
    encrypted_file = 'archivo_encriptado.bin'
    decrypted_file = 'archivo_descifrado.txt'
    
    # Cifrar el archivo
    encrypt_file(input_file, encrypted_file, key16)
    print(f"Archivo {input_file} cifrado en {encrypted_file}.")
    
    # Descifrar el archivo
    decrypt_file(encrypted_file, decrypted_file, key16)
    print(f"Archivo {encrypted_file} descifrado en {decrypted_file}.")







# Aqui empieza el RSA----------------------------------------------------------------------------------------------


# Version limpia en funciones de rsa.py

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def generate_rsa_keys():
    key = RSA.generate(3072)
    return key, key.public_key()

def rsa_encrypt(data_to_encrypt, public_key):
    cipher_rsa = PKCS1_OAEP.new(public_key)
    return cipher_rsa.encrypt(data_to_encrypt)

def rsa_decrypt(encrypted_data, private_key):
    cipher_rsa = PKCS1_OAEP.new(private_key)
    return cipher_rsa.decrypt(encrypted_data)

def export_keys(private_key, public_key):
    private_key_pem = private_key.export_key()
    public_key_pem = public_key.export_key()

    # ...
    # sentencias de la base de datos para almacenarlas
    # ...

    # Para ver si funciona bien la importacion
    # Guardar las claves en archivos
    with open("private_key.pem", "wb") as f:
        f.write(private_key_pem)
        
    with open("public_key.pem", "wb") as f:
        f.write(public_key_pem)

def import_keys():
    # Cargar la clave privada
    with open("private_key.pem", "rb") as f:
        private_key_pem = f.read()
        private_key = RSA.import_key(private_key_pem)

    # Cargar la clave pública
    with open("public_key.pem", "rb") as f:
        public_key_pem = f.read()
        public_key = RSA.import_key(public_key_pem)

    return private_key, public_key

if __name__ == "__main__":
    data_to_encrypt = key16 #key16 es la clave aleatoria de 16 bytes generada en la parte de AES128

    key, public_key = generate_rsa_keys()
    encrypted_data = rsa_encrypt(data_to_encrypt, public_key)
    decrypted_data = rsa_decrypt(encrypted_data, key)

    # Al ser la clave publica, publica (jajaja) no se asegura la autenticidad del mensaje por lo que seria
    # interesante utilizar una firma digital, con sha-256 o algo por el estilo calcular un hash antes y despues
    # del cifrado/descifrado y luego comparar

    export_keys(key, public_key)
    # Importar las claves
    private_key, public_key = import_keys()










# Función para cifrar la clave privada RSA usando AES128
def encrypt_private_key_with_aes(private_key_pem, aes_key):
    # Padding de la clave privada para que sea múltiplo del tamaño de bloque de AES
    padded_private_key = pad(private_key_pem, AES.block_size)

    # Cifrar la clave privada con AES128
    cipher = AES.new(aes_key, AES.MODE_ECB)
    encrypted_private_key = cipher.encrypt(padded_private_key)

    return encrypted_private_key

# Función para descifrar la clave privada RSA usando AES128
def decrypt_private_key_with_aes(encrypted_private_key, aes_key):
    cipher = AES.new(aes_key, AES.MODE_ECB)
    decrypted_private_key_padded = cipher.decrypt(encrypted_private_key)

    # Quitar el padding
    private_key_pem = unpad(decrypted_private_key_padded, AES.block_size)

    return private_key_pem



# Cifrar clave privada RSA con AES128
private_key_pem = key.export_key()
encrypted_private_key = encrypt_private_key_with_aes(private_key_pem, key16)


# Descifrar la clave privada con AES128
decrypted_private_key_pem = decrypt_private_key_with_aes(encrypted_private_key, key16)
decrypted_private_key = RSA.import_key(decrypted_private_key_pem)






# # COMPROBACION DE EJEMPLO DE CIFRADO DE LA CLAVE PRIVADA RSA CON AES (SI SE QUIERE COMPROBAR, SE DEBE PONER EL MENSAJE_EJEMPLO.TXT DENTRO DE LA CARPETA FUNCTIONS POR EL MOMENTO)

# # Paso 1: Generar claves RSA
# key, public_key = generate_rsa_keys()

# # Exportar la clave privada original en formato PEM
# private_key_pem_original = key.export_key()

# # Generar una clave AES aleatoria de 16 bytes (AES128)
# key16 = os.urandom(16)

# # Paso 2: Cifrar la clave privada con AES128
# encrypted_private_key = encrypt_private_key_with_aes(private_key_pem_original, key16)
# print("Clave privada cifrada correctamente.")

# # Paso 3: Descifrar la clave privada con AES128
# decrypted_private_key_pem = decrypt_private_key_with_aes(encrypted_private_key, key16)
# print("Clave privada descifrada correctamente.")

# # Paso 4: Comparar la clave privada original con la descifrada
# if private_key_pem_original == decrypted_private_key_pem:
#     print("La clave privada descifrada coincide con la original. ¡Cifrado y descifrado correctos!")
# else:
#     print("Error: La clave privada descifrada no coincide con la original.")
