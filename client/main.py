import requests, json
from functions.aes import encrypt_file, decrypt_file,generate_aes_key
from functions.rsa import rsa_encrypt, generate_rsa_keys


global server
server = "http://127.0.0.1:5000"

file_aes_key = generate_aes_key()

encrypted_file = "file_encrypt.txt"
encode_file = "file_encode.txt"

encrypt_file(r"C:\Users\donsi\Desktop\MALFA\COSAS DE STREAMER\YOUTUBE\VIDEOS\HOLLOW RADIANTE\OBBLOBBLE\OBBLOBBLE.mp4", encrypted_file, encode_file, file_aes_key)


decrypted_file = "decrypted_file.mp4"

decrypt_file(r"C:\Users\donsi\Desktop\MALFA\UNI\AÑO 3\CS\P1\CyS-P1\file_encode.txt", decrypted_file, file_aes_key)

#print(json.loads(r.text)[1]["user"])

# ui_prueba.seleccionar_archivo()

