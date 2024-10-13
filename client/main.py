import requests, json
import secrets
from functions.aes import encrypt_file, decrypt_file
#r = requests.get('http://127.0.0.1:5000/users')

# for s in json.loads(r.text):
#     print(s,"\n")

file_aes_key = secrets.token_bytes(16)

encrypted_file = "file_encrypt.txt"

encrypt_file(r"C:\Users\donsi\Desktop\MALFA\COSAS DE STREAMER\CLIPS\HOLLOW\VENGAMOSCA MUY RÁPIDO.mp4", encrypted_file, file_aes_key)


decrypted_file = "decrypted_file.mp4"
deco_file = "file_deco.txt"

decrypt_file(r"C:\Users\donsi\Desktop\MALFA\UNI\AÑO 3\CS\P1\CyS-P1\file_encrypt.txt", deco_file, decrypted_file, file_aes_key)

#print(json.loads(r.text)[1]["user"])

# ui_prueba.seleccionar_archivo()

