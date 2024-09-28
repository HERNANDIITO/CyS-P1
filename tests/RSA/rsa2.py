# Código basado en: https://medium.com/coinmonks/rsa-encryption-and-decryption-with-pythons-pycryptodome-library-94f28a6a1816
# Documentacion de Pycryptodome RSA: https://pycryptodome.readthedocs.io/en/latest/src/public_key/rsa.html#Crypto.PublicKey.RSA.RsaKey
# Import necessary modules from pycryptodome
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

import base64

# Paso 2: Generamos una nueva clave RSA
# Creamos un par de claver RSA de 3072 bits, en el codigo de medium.com se utiliza una clave de 2048 bits
# pero leyendo la especificacion del NIST, pagina 55 del documento Recomendaciones del NIST para el manejo de claves - Mayo 2020
# diponible en info.md, y la documentacion de Pycryptodome es recomendable ir pasando a RSA 3072, aunque
# hasta 2027 aun se puede seguir utilizando (usage period) y su security life se extiende hasta 2031.

# Aun asi, le quiero preguntar al profesor sobre esto
key = RSA.generate(3072)





# Estas funciones las pongo simplemente a modo de demostracion, para facilitar la compresion
print("Dimensiones de la clave en bits:", key.size_in_bits());
print("Dimensiones de la clave en bytes:", key.size_in_bytes());

# Si queremos imprimir las claves y no ves cosas sin sentido debemos esportarla previamente a formato PEM, 
# para mas informacion consultar la seccion extra de info.md
# Exportamos la clave privada en formato PEM
private_key_pem = key.export_key()
# private_key_pem_passphrase = key.export_key(passphrase=b"ThisIsA16ByteKey", 
#                                             pkcs=8, 
#                                             protection='PBKDF2WithHMAC-SHA512AndAES256-CBC',
#                                             prot_params={'iteration_count':131072})
# Exportamos la clave pública en formato PEM
public_key_pem = key.publickey().export_key()

# Las claves están en formato PEM, listas para ser almacenadas en la base de datos
print(private_key_pem.decode('utf-8'))
# print(private_key_pem_passphrase.decode('utf-8'))
print(public_key_pem.decode('utf-8'))

# Importante saber que key es por defecto la clave privada, para acceder a la publica debemos hacer key.publickey()
print("¿Es una clave RSA privada key?:", key.has_private())
print("¿Es una clave RSA privada key.publickey()?:", key.publickey().has_private())





# Obtenemos la clave publica 
public_key = key.publickey()

# Paso 3: Encripta utilizando la clave publica
# Creamos un objeto de cifrado PKCS1_OAEP con la clave pública para encriptar
datos_de_entrada = b"ThisIsA16ByteKey"
cifrado_rsa = PKCS1_OAEP.new(public_key)

# Encriptamos con la clave publica
datos_cifrados = cifrado_rsa.encrypt(datos_de_entrada)


print("Datos cifrados:", datos_cifrados)
datos_cifrados_base64 = base64.b64encode(datos_cifrados).decode('utf-8')
print("Datos encriptados base64:", datos_cifrados_base64)


# Paso 4: Desencriptar con la clave privada
# Creamos un objeto de cifrado PKCS1_OAEP con la clave privada para descifrar
cifrado_rsa = PKCS1_OAEP.new(key)
datos_descifrados = cifrado_rsa.decrypt(datos_cifrados)


# Mostramos el resultado en utf-8
print("Datos desencifrados:", datos_descifrados.decode("utf-8"))

