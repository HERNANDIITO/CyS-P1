from functions.rsa import rsa_encrypt, generate_rsa_keys
from functions.aes import generate_aes_key

# Preparativos para la funcion

rsa_private_key, rsa_public_key = generate_rsa_keys()
aes_key = generate_aes_key()

# Funciona bien

rsa = rsa_encrypt(aes_key, rsa_public_key)
print(rsa)

# Falla

try:
    rsa = rsa_encrypt(str(190 * 190), rsa_public_key)
except Exception as e:
    print(e.args[0], "|", e.args[1])
    