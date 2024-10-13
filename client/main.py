import requests, json
import secrets
from functions.aes import encrypt_file, decrypt_file
from functions.rsa import rsa_encrypt, generate_rsa_keys


global server
server = "http://127.0.0.1:5000"

file_aes_key = secrets.token_bytes(16)

encrypted_file = "file_encrypt.txt"
encode_file = "file_encode.txt"

encrypt_file(r"C:\Users\donsi\Downloads\a.txt", encrypted_file, encode_file, file_aes_key)


decrypted_file = "decrypted_file.txt"
deco_file = "file_deco.txt"

decrypt_file(r"C:\Users\donsi\Desktop\MALFA\UNI\AÑO 3\CS\P1\CyS-P1\file_encode.txt", deco_file, decrypted_file, file_aes_key)

#print(json.loads(r.text)[1]["user"])

# ui_prueba.seleccionar_archivo()

