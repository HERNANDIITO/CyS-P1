
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import secrets

    #Genera una clave AES de 16 bytes (128 bits).
# def generate_aes_key():
#     return secrets.token_bytes(16)

#    Descifra un archivo utilizando AES en modo ECB.
# def decrypt_file(input_file, output_file, aes_key):
#     with open(input_file, 'rb') as f:
#         encrypted_data = f.read()

#     encrypted_data = base64.b64decode(encrypted_data)
#     cipher = AES.new(aes_key, AES.MODE_ECB)
#     decrypted_data = cipher.decrypt(encrypted_data)
#     original_data = unpad(decrypted_data, AES.block_size)

#     with open(output_file, 'wb') as f:
#         f.write(original_data)

    #Cifra una clave privada RSA utilizando AES128.
def encrypt_private_key_with_aes(private_key_pem, aes_key):
    padded_private_key = pad(private_key_pem, AES.block_size)
    cipher = AES.new(aes_key, AES.MODE_ECB)
    encrypted_private_key = base64.b64encode(cipher.encrypt(padded_private_key))
    return encrypted_private_key

    #Descifra una clave privada RSA utilizando AES128.
def decrypt_private_key_with_aes(encrypted_private_key_pem, aes_key):
    encrypted_private_key_pem = base64.b64decode(encrypted_private_key_pem)
    cipher = AES.new(aes_key, AES.MODE_ECB)
    decrypted_private_key_pem = cipher.decrypt(encrypted_private_key_pem)
    private_key_pem = unpad(decrypted_private_key_pem, AES.block_size)
    return private_key_pem



# Codigos de encrypt y decrypt por bloques (de prueba)
def encrypt_file(input_file, output_file, encoded_file, aes_key, block_size=16):
    cipher = AES.new(aes_key, AES.MODE_ECB)


    # Encriptar
    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        while True:
            block = f_in.read(AES.block_size)
            if len(block) == 0:  # Fin del archivo
                break

            elif len(block) % AES.block_size != 0:  # Rellenar el último bloque si es necesario
                block = pad(block, AES.block_size)
            
            encrypted_block = cipher.encrypt(block)
            
            f_out.write(encrypted_block)


    # Codificar
    with open(output_file, 'rb') as f_in, open(encoded_file, 'wb') as f_out:
        while True:
            block = f_in.read(3 * 1024 * 1024)
            if len(block) == 0:  # Fin del archivo
                break

            encoded_block_b64 = base64.b64encode(block) # Codificar en base64
            
            f_out.write(encoded_block_b64)


def decrypt_file(input_file, decoded_input_file, output_file, aes_key, block_size=16):

    cipher = AES.new(aes_key, AES.MODE_ECB)

    # Decodificar
    with open(input_file, 'rb') as f_in, open(decoded_input_file, 'wb') as f_out:
        buffer = b""  # Buffer para manejar fragmentos incompletos de Base64
        
        while True:
            block = f_in.read(4 * 1024 * 1024)

            if len(block) == 0:  # Fin del archivo
                break

            block = buffer + block  # Combinar con los restos del bloque anterior
            remainder = len(block) % 4  # Determinar si quedó incompleto

            if remainder != 0:
                buffer = block[-remainder:]  # Guardar lo que sobró en el buffer
                block = block[:-remainder]  # Formar un bloque con todo menos lo que sobró
            else:
                buffer = b""
            
            block = base64.b64decode(block)
            
            f_out.write(block)




    # Desencriptar
    with open(decoded_input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        while True:

            block = f_in.read(AES.block_size)

            if len(block) == 0:  # Fin del archivo
                break
            
            #block = base64.b64decode(block)
            decrypted_block = cipher.decrypt(block)

            try:
                decrypted_block = unpad(decrypted_block, AES.block_size)
            except ValueError:
                pass  # Unpad solo si es el último bloque con padding
            
            f_out.write(decrypted_block)    


# COMENTARIO PARA VER SI ASÍ ME DEJA HACER COMMIT LA BASURA DEL GITHUB