import secrets
import string

# Geredor de contraseñas seguras formadas por letras ASCII estándar a-Z, números 0-9 y signos de
# puntuacion !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
def generate_secure_password(length=16):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for i in range(length))

passphrase = generate_secure_password()
print(f"Generated passphrase: {passphrase}")


def register(email, password): 


def login(email, password):