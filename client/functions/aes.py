
import base64
from Crypto.Cipher import AES
import secrets


    #Genera una clave AES de 16 bytes (128 bits).
def generate_aes_key():
    return secrets.token_bytes(16)


# Cifra una clave privada RSA utilizando AES128 en modo CTR.
def encrypt_private_key_with_aes(private_key_pem, aes_key):
    # Generar un nonce único de 12 bytes (12 es un buen punto medio para proporcionar buean seguridad y dejar 4 bytes para la clave privada)
    nonce = secrets.token_bytes(12)
    
    # Crear el cifrador en modo CTR
    cipher = AES.new(aes_key, AES.MODE_CTR, nonce=nonce)
    
    # Cifrar los datos
    encrypted_private_key = cipher.encrypt(private_key_pem)
    
    # Codificar el resultado como Base64 para facilitar el transporte
    # Incluye el nonce para poder usarlo al descifrar
    encrypted_private_key_with_nonce = base64.b64encode(nonce + encrypted_private_key)
    return encrypted_private_key_with_nonce


def decrypt_private_key_with_aes(encrypted_private_key_pem, aes_key):
    # Convertir aes_key a bytes si es una cadena
    if isinstance(aes_key, str):
        aes_key = aes_key.encode("utf-8")
    
    # Decodificar los datos base64
    encrypted_data = base64.b64decode(encrypted_private_key_pem)
    
    # Separar el nonce del contenido cifrado
    nonce = encrypted_data[:12]  # El nonce siempre es los primeros 15 bytes
    encrypted_private_key = encrypted_data[12:]
    
    # Crear el cifrador en modo CTR usando el mismo nonce
    cipher = AES.new(aes_key, AES.MODE_CTR, nonce=nonce)
    
    # Descifrar los datos
    decrypted_private_key_pem = cipher.decrypt(encrypted_private_key)
    return decrypted_private_key_pem
















# ENCRIPTADO Y DESENCRIPTADO DE ARCHIVOS-------------------------------------------------------------------------------------------------------------------------------






def encrypt_file(input_file, output_file, encoded_file, aes_key):
    # Asegurarse de que la clave AES está en formato bytes
    if isinstance(aes_key, str):
        aes_key = aes_key.encode('utf-8')

    # Generar un nonce adecuado de 12 bytes (12 por si se da el caso de un archivo gigantesco, y dado que 12 bytes de nonce es mas que seguro y es el tamanyo recomendado en varios estandares modernos)
    nonce = secrets.token_bytes(12)

    # Crear el cifrador en modo CTR
    cipher = AES.new(aes_key, AES.MODE_CTR, nonce=nonce)

    # Leer y cifrar el contenido del archivo en partes
    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        f_out.write(nonce)  # Guardar el nonce al principio del archivo de salida

        while True:
            chunk = f_in.read(64 * 1024)  # Leer en trozos de 64 KB
            if not chunk:
                break
            encrypted_chunk = cipher.encrypt(chunk)
            f_out.write(encrypted_chunk)

    # Codificar el archivo cifrado en Base64 y guardarlo
    with open(output_file, 'rb') as f_in, open(encoded_file, 'wb') as f_out:
        encoded_data_b64 = base64.b64encode(f_in.read())
        f_out.write(encoded_data_b64)


# Descifra un archivo codificado en Base64 utilizando AES en modo CTR

def decrypt_file(input_file, output_file, aes_key):
    # Leer el archivo codificado en Base64 y decodificarlo
    with open(input_file, 'rb') as f:
        base64_data = f.read()  # Leer el contenido del archivo en Base64
        binary_data = base64.b64decode(base64_data)  # Decodificar Base64 a binario

    # Extraer el nonce de los primeros 12 bytes
    nonce = binary_data[:12]  # Los primeros 12 bytes son el nonce
    encrypted_data = binary_data[12:]  # El resto es el contenido cifrado

    # Crear el cifrador en modo CTR usando el nonce extraído
    cipher = AES.new(aes_key, AES.MODE_CTR, nonce=nonce)
    
    # Descifrar los datos
    decrypted_data = cipher.decrypt(encrypted_data)
    
    # Guardar los datos descifrados en el archivo de salida
    with open(output_file, 'wb') as f:
        f.write(decrypted_data)



