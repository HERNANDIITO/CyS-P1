import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# Generar un par de claves RSA de 2048 bits (pública y privada).
def generate_rsa_keys():
    private_key = RSA.generate(2048)
    public_key = private_key.public_key()
    return private_key, public_key

# Cifrar datos utilizando la clave pública RSA y el esquema de relleno (padding) Optimal Asymmetric Encryption Padding OAEP.
def rsa_encrypt(data, public_key):
    cipher_rsa = PKCS1_OAEP.new(public_key)
    return base64.b64encode(cipher_rsa.encrypt(data))

# Descifra datos utilizando la clave privada RSA con OAEP durante el descifrado validamos el relleno y la 
# estructura del mensaje cifrado y eliminamos el padding.
def rsa_decrypt(encrypted_data, private_key):
    encrypted_data = base64.b64decode(encrypted_data)
    cipher_rsa = PKCS1_OAEP.new(private_key)
    return cipher_rsa.decrypt(encrypted_data)

#Exporta las claves RSA a archivos PEM.
def export_keys(private_key, public_key):
    private_key_pem = private_key.export_key()
    public_key_pem = public_key.export_key()

    return private_key_pem, public_key_pem
    # ...
    # sentencias de la base de datos para almacenarlas
    # ...

    # Para ver si funciona bien la importacion
    # Guardar las claves en archivos

    # with open("private_key.pem", "wb") as f:
    #     f.write(private_key_pem)
        
    # with open("public_key.pem", "wb") as f:
    #     f.write(public_key_pem)

# Importa las claves RSA desde archivos PEM.
def import_keys():
    with open("private_key.pem", "rb") as f:
        private_key_pem = f.read()
        private_key = RSA.import_key(private_key_pem)

    with open("public_key.pem", "rb") as f:
        public_key_pem = f.read()
        public_key = RSA.import_key(public_key_pem)

    return private_key, public_key
