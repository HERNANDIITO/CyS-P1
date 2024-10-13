import requests, json
import secrets
from functions.aes import encrypt_file, decrypt_file
from functions.rsa import rsa_encrypt, generate_rsa_keys
from functions.aes import generate_aes_key

global server
server = "http://127.0.0.1:5000"

file_aes_key = secrets.token_bytes(16)

encrypted_file = "file_encrypt.txt"

encrypt_file(r"C:\Users\donsi\Desktop\MALFA\COSAS DE STREAMER\CLIPS\HOLLOW\VENGAMOSCA MUY RÁPIDO.mp4", encrypted_file, file_aes_key)


decrypted_file = "decrypted_file.mp4"
deco_file = "file_deco.txt"

decrypt_file(r"C:\Users\donsi\Desktop\MALFA\UNI\AÑO 3\CS\P1\CyS-P1\file_encrypt.txt", deco_file, decrypted_file, file_aes_key)