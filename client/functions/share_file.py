from functions.user import User
import functions.rsa as rsa
import functions.file_requests as file_request
from functions.result import Result


def share(sharedFileId, recieverId, transmitter: User, recieverPublicRSAKey, AESKey): 
    try:

        # Obtenemos la clave RSA privada del usuario
        transmitterPrivateRSAKey = transmitter.privateRSA
        importedRSAKey = rsa.import_public_key(recieverPublicRSAKey) 

        # Desciframos la clave AES128 utilizada para cifrar el archivo con la clave privada RSA
        decryptedAESKey = rsa.rsa_decrypt(AESKey, transmitterPrivateRSAKey)

        # Cifrarmos la clave AES con la clave publica RSA del reciever.
        encryptedAESKeyforReciever = rsa.rsa_encrypt(decryptedAESKey, importedRSAKey)

        # Almacenamos los datos en la bdaz
        userId = transmitter.userId
        return file_request.share_file(sharedFileId, userId, recieverId, encryptedAESKeyforReciever.decode("utf-8"))

    except Exception as e:
        return Result(500, f"Error al compartir archivo: {e}", False, "")
