import os
import requests
from functions.user import User
import functions.aes as aes
import functions.rsa as rsa
import functions.file_requests as file_request
import encrypt_decrypt

global server
server = "http://127.0.0.1:5000"


def share(sharedFileId, recieverId, transmitter: User): 
    try:
        # select publicRSA from users where userId = recieverId
        # select AESKey from files where fileId = sharedFileId
        recieverPublicRSAKey = '';
        AESKey = '';

        # Obtenemos la clave RSA privada del usuario
        transmitterPrivateRSAKey = transmitter.privateRSA

        # Desciframos la clave AES128 utilizada para cifrar el archivo con la clave privada RSA
        decryptedAESKey = rsa.rsa_decrypt(AESKey, transmitterPrivateRSAKey)

        # Cifrarmos la clave AES con la clave publica RSA del reciever.
        encryptedAESKeyforReciever = rsa.rsa_encrypt(decryptedAESKey, recieverPublicRSAKey)

        # Almacenamos los datos en la bd
        userId = transmitter.userId
        file_request.share_file(sharedFileId, userId, recieverId, encryptedAESKeyforReciever)

    except Exception as e:
        print(f"Error al compartir archivo: {e}")
        raise