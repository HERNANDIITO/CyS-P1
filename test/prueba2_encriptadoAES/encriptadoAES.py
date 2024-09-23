# https://www.youtube.com/watch?v=GYCVmMCRmTM&t=247s
# https://pycryptodome.readthedocs.io/en/latest/src/cipher/aes.html

from Crypto.Cipher import AES
from secrets import token_bytes

data = b"El mensaje que se desea encriptar, holaa caralolaaa."
key = b'Sixteen byte key'
key2 = token_bytes(16)
print("key2:", key2)
print("key:", key)

cipher = AES.new(key, AES.MODE_EAX)

nonce = cipher.nonce
ciphertext, tag = cipher.encrypt_and_digest(data)
print("ciphertext:", ciphertext)
print("tag:", tag)

cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
plaintext = cipher.decrypt(ciphertext)
try:
    cipher.verify(tag)
    print("El mensaje desencriptado es:", plaintext)
except ValueError:
    print("Key incorrecta o mensaje corrupto.")