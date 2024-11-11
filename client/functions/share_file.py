import os
import requests
from functions.user import User
import functions.aes as aes
import functions.rsa as rsa
import functions.file_requests as file_request
import encrypt_decrypt

global server
server = "http://127.0.0.1:5000"


def share(sharedFileId, recieverId, user: User): 

    # get public_rsa from users where id = user_id
    # get file_name, encrypted_file, file_aes_key_encrypted, file_type from files where id = file_id

    decrypted_file =  encrypt_decrypt.decrypt(user, file_name, encrypted_file, file_aes_key_encrypted, file_type)

    transmitterId = User.user_id
    encrypt_decrypt.share_encrypt(sharedFileId, transmitterId, recieverId, decrypted_file, public_rsa_reciever)
