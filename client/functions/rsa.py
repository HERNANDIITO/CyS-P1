import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256

# Generar un par de claves RSA de 2048 bits (pública y privada).
def generate_rsa_keys():
    private_key = RSA.generate(2048)
    public_key = private_key.public_key()
    return private_key, public_key

# Cifrar datos utilizando la clave pública RSA y el esquema de relleno (padding) Optimal Asymmetric Encryption Padding OAEP.
def rsa_encrypt(data, public_key):
    try:
        cipher_rsa = PKCS1_OAEP.new(public_key, hashAlgo=SHA256)
        return base64.b64encode(cipher_rsa.encrypt(data))
    except ValueError as e:
        print("Error, mensaje demasiado largo máximo 190 bytes: ", e)
        return None
    except Exception as e:
        print("Lo sentimos, se ha producido un error innesperado durante la encriptación con RSA: ", e)
        return None

# Descifra datos utilizando la clave privada RSA con OAEP durante el descifrado validamos el relleno y la 
# estructura del mensaje cifrado y eliminamos el padding.
def rsa_decrypt(encrypted_data, private_key):
    try:
        encrypted_data = base64.b64decode(encrypted_data)
        cipher_rsa = PKCS1_OAEP.new(private_key, hashAlgo=SHA256)
        return cipher_rsa.decrypt(encrypted_data)
    except ValueError as e:
        print("Error, el texto cifrado tiene una longitud incorrecta o ha fallado la comprobación de integridad: ", e)
        return None
    except TypeError as e:
        print("Error, la clave RSA no tiene la mitad de clave privada: ", e)
        return None
    except Exception as e:
        print("Lo sentimos, se ha producido un error innesperado durante la desencriptación con RSA: ", e)
        return None

#Exporta las claves RSA a archivos PEM.
def export_keys(private_key, public_key):
    try:
        private_key_pem = private_key.export_key()
        public_key_pem = public_key.export_key()

        return private_key_pem, public_key_pem
    except ValueError as e:
        print("Error, formato desconocido: ", e)
        return None, None
    except Exception as e:
        print("Lo sentimos, se ha producido un error innesperado durante la exportación de claves RSA: ", e)
        return None, None

# Importa las claves RSA desde archivos PEM.
def import_public_key(public_key_pem):
    public_key = RSA.import_key(public_key_pem)

    return public_key

def import_private_key(private_key_pem):
    private_key = RSA.import_key(private_key_pem)

    return private_key
