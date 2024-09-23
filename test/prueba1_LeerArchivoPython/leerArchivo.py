# # Abrimos el archivo binario
# file = open("gatos.jpeg", "rb")
# # Leemos el archivo binario y obtenemos los bytes 0-255
# data = file.read()

# # Convertir cada byte en su representación binaria y luego unirlos
# # .join se utiliza para concatenar, con '' indicamos que las cadenas unidas deben separarse por una cadena vacía, 
# # es decir, que estarán unidas. 
# # con format(byte, '08b') damos formato a cada byte de data en formato binario por la b
# # de 8 posiciones por el 8 las cuales si no se rellenan se completaran con ceros a la izquieda
# binary_data = ''.join(format(byte, '08b') for byte in data)

# # Imprimimos el archivo en formato binario
# print(binary_data)

# # Cerramos el archivo
# file.close()

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

# Leer el archivo binario (gatos.jpeg)
with open("hola.txt", "rb") as file:
    data = file.read()
print(data)
# Generar una clave AES de 16, 24 o 32 bytes (usaremos 16 para AES-128)
key = get_random_bytes(16)

print(key)

# Crear el objeto de cifrado AES en modo ECB
cipher = AES.new(key, AES.MODE_ECB)

# Aplicar padding a los datos para que sea un múltiplo de 16 bytes
padded_data = pad(data, AES.block_size)

# Encriptar los datos
encrypted_data = cipher.encrypt(padded_data)

# Guardar los datos encriptados en un archivo
with open("gatos_encrypted_ecb.txt", "wb") as encrypted_file:
    encrypted_file.write(encrypted_data)

print("Archivo encriptado correctamente con AES-ECB.")
