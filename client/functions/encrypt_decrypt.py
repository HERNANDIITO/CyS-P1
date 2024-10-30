import os
import requests
from functions.user import User
import functions.aes as aes
import functions.rsa as rsa
import functions.file_requests as file_request

global server
server = "http://127.0.0.1:5000"

def get_file_name_and_type(file_path):
    try:
        file_name = os.path.basename(file_path)
        file = os.path.splitext(file_name)
        return file[0], file[1]
    except FileNotFoundError:
        print("Error: No se encontró el archivo especificado.")

# FUNCIONES DE CONTACTO CON LA BD----------------------------------------------------------------------------------------------------------------


# def store_encrypted_data_in_db(file_name, encrypted_file, file_aes_key_encrypted, rsa_public_key_pem, encrypted_rsa_private_key_pem, rsa_aes_key, file_type):
#     # obtener userId, date con SYSDATE?, fileId creo que no hace falta
#     file_data = {
#         'fileName': file_name,
#         'encryptedFile': encrypted_file,
#         'AESKey': file_aes_key_encrypted,
#         'publicRSA':  rsa_public_key_pem,
#         'privateRSA': encrypted_rsa_private_key_pem,
#         'rsaAESKey': rsa_aes_key,  # deberiamos de protegerla de algun modo
#         'fileType': file_type
#     }

#     save_new_file(file_data)


# def get_encrypted_data_from_db(file_path):
    


# FUNCIONES DE ENCRIPTADO Y DESENCRIPTADO--------------------------------------------------------------------------------------------------------

# Funcion principal para gestionar el cifrado de archivos multimedia
def encrypt(file_path, user): 
    # Generamos una clave AES128 para cifrar el archivo
    file_aes_key = aes.generate_aes_key()

    # UN ERROR SI EL ARCHIVO NO SE ENCUENTRA ESTARÍA CHULO
    # Obtenemos el nombre y extension del fichero
    file_name, file_type = get_file_name_and_type(file_path)

    # Creamos el archivo de salida, resultado cifrado
    encrypted_file = "file_encrypted.txt"
    b64encoded_encrypted_file = "b64encoded_encrypted_file.txt"

    # Ciframos el archivo con AES128
    aes.encrypt_file(file_path, encrypted_file, b64encoded_encrypted_file, file_aes_key)


    # ESTO AQUÍ NO SE HACE, SE DEBEN RECUPERAR CON EL ID DEL USUARIO AL INICIAR SESION/REGISTRASTE, DEBERIA DE TENERLAS EN LOCAL TRAS FINALIZAR CUALQUIERA DE ESTAS OPERACIONES HASTA QUE CIERRE SESION 
    # Generamos una pareja de claves pública-privada RSA 2048 bits
    # rsa_private_key, rsa_public_key = rsa.generate_rsa_keys()
    rsa_private_key = user.privateRSA
    rsa_public_key = user.publicRSA

    # Ciframos la clave AES128 con la que hemos cifrado el archivo con la clave pública RSA
    file_aes_key_encrypted = rsa.rsa_encrypt(file_aes_key, rsa_public_key)

    # NO HACE FALTA
    # Exportamos las claves RSA a formato PEM
    # rsa_private_key_pem, rsa_public_key_pem = rsa.export_keys(rsa_private_key, rsa_public_key)

    # TAMPOCO HACE FALTA YA, ESTA CLAVE AES ES AHORA LA SEGUNDA PARTE DEL HASH CON SHA3 DE LA CONTRASEÑA, Y ESO YA SE HA HECHO ANTES
    # Protegemos la clave privada RSA con AES128
    # rsa_aes_key = user.aesHash
    # encrypted_rsa_private_key_pem = aes.encrypt_private_key_with_aes(rsa_private_key_pem, rsa_aes_key)

    # Almacenamos la informacion en la base de datos
    # FALTA LA PETICION
    # store_encrypted_data_in_db(file_name, encrypted_file, file_aes_key_encrypted, file_type)

    # def upload(self, file: FileStorage, path: str, aesKey: str, publicRSA: str, privateRSA: str, userId: int) -> Result:
 
    subir_archivo_result = requests.post(server+"/users/upload", json = {
        "file": encrypted_file,
        "path": ,
        "aesKey": file_aes_key,
        "userId": user.userId
    })
    
    login_result_json = json.loads(login_result.text)
    
    print("PRE 200!")
    print( "code", json.loads(login_result.text) )
    print( "email", email )
    print( "password", password )
    if(str(json.loads(login_result.text)["code"]) == "200"):
        
        # hacer una peticion que me devuelva la clave privada del usuario
        userID      = login_result_json["body"]["userID"]
        privateRSA  = login_result_json["body"]["privateRSA"]
        publicRSA   = login_result_json["body"]["publicRSA"]
        
        # desencriptar con aes la pass_hash_part2, descifrar y guardar en local
        
        # Las claves no van y no puedo mas :C
        importedPublicKey  = import_public_key(public_key_pem = publicRSA)
        
        decryptedPrivateKey = decrypt_private_key_with_aes(encrypted_private_key_pem = privateRSA, aes_key = aes_key)
        
        importedPrivateKey = import_private_key(private_key_pem = decryptedPrivateKey)
            
        user = User( userId = userID, privateRSA = importedPrivateKey, publicRSA = importedPublicKey, aesHash = aes_key )
        
        return user
    
    else:
        return None


# Funcion principal para gestionar el descifrado de archivos multimedia
def decrypt(file_path, user: User, file_name, encrypted_file, file_aes_key_encrypted, file_type):

    # PETICION PARA RECUPERAR EL ARCHIVO DEL SERVIDOR
    # Recuperamos la información almacenada en la base de datos
    #file_name, encrypted_file, file_aes_key_encrypted, file_type = get_encrypted_data_from_db(file_path)

    # NO HACE FALTA YA ESTA EN LOCAL DESDE QUE SE REGISTRA/INICIA SESION (si SE HA HEHCO ANTES CLARO)
    # Desciframos la clave privada RSA con la clave AES128
    # rsa_private_key_pem = decrypt_private_key_with_aes(encrypted_rsa_private_key_pem, rsa_aes_key)

    # YA DEBERÍA DE ESTAR HECHO
    # Convertimos la clave privada RSA desde el formato PEM
    # rsa_private_key = import_private_key(rsa_private_key_pem)
    rsa_private_key = user.privateRSA

    # Desciframos la clave AES128 utilizada para cifrar el archivo con la clave privada RSA
    file_aes_key = rsa_decrypt(file_aes_key_encrypted, rsa_private_key)

    # Desciframos el archivo con la clave AES128
    decrypted_file = file_name + file_type
    decrypt_file(encrypted_file, decrypted_file, file_aes_key)

    # return decrypted_file

    # print(f"Archivo descifrado correctamente y guardado como {decrypted_file}")
    # DEBERIAMOS DE PREGUNTARLE AL USUARIO DÓNDE DESEA DESCARGAR SUS ARCHIVOS??? EN FIN, CREO QUE ESO ES TODO POR AQUI
    
# NECESITAMOS PARA LAS CLAVES RSA QUE LAS DEVUELVA USER_AUTH, LO MÁS LIMPIO CREO QUE ES QUE 
# LAS FUNCIONES DE USER_AUTH UNICAMENTE SE ENCARGUEN DE QUE LAS CLAVES LLEGEN HASTA ESTE ARCHIVO Y UNA VEZ AQUI
# HACER UNA FUNCION QUE SE ENCARGUE DE DESCIFRAR LAS CLAVES RSA DE LAS VARIABLES PARA LUEGO USARLAS EN LA FUNCIONES ENCRYPT/DECRYPT

# main para hacer pruebas
if __name__ == "__main__":
    encrypt(r"C:\Users\Laura\Desktop\Captura de pantalla 2024-10-10 172227.png")
