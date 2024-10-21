import secrets
import string
from Crypto.Hash import SHA3_256

global server
server = "http://127.0.0.1:5000"

# Geredor de contraseñas seguras formadas por letras ASCII estándar a-Z, números 0-9 y signos de
# puntuacion !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
def generate_secure_password(length=16):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for i in range(length))

passphrase = generate_secure_password()
print(f"Generated passphrase: {passphrase}")


def register(email, password): 
    print(email, password)


def login(email, password):
    respuesta = ''

    if(email == '' or password == ''):
        respuesta = 'Por favor, introduce un email y contraseña'

    # Se podrian testear expresiones regular
    #     regex = re.compile(r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")

    # def isValid(email):
    #     if re.fullmatch(regex, email):
    #         print("Valid email")
    #     else:
    #         print("Invalid email")
    if "@" not in email:
        respuesta = 'Por favor, introduce un email válido'

    pass_hash = SHA3_256.new()
    pass_hash.update(bytes(password, encoding="utf-8"))
    
    pass_hash_hex = pass_hash.hexdigest()

    pass_hash_part1 = pass_hash_hex[:int(len(pass_hash_hex)/2)]
    pass_hash_part2 = pass_hash_hex[-int(len(pass_hash_hex)/2):]

    print(pass_hash_hex)
    print(pass_hash_part1)
    print(pass_hash_part2)

    
if __name__ == "__main__":
    login("uncorreo@gamil.com", "12345678")

