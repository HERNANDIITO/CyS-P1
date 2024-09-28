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
    data_to_encrypt = b"ThisIsA16ByteKey"

    key, public_key = generate_rsa_keys()
    encrypted_data = rsa_encrypt(data_to_encrypt, public_key)
    decrypted_data = rsa_decrypt(encrypted_data, key)

    # Al ser la clave publica, publica (jajaja) no se asegura la autenticidad del mensaje por lo que seria
    # interesante utilizar una firma digital, con sha-256 o algo por el estilo calcular un hash antes y despues
    # del cifrado/descifrado y luego comparar

    export_keys(key, public_key)
    # Importar las claves
    private_key, public_key = import_keys()




    