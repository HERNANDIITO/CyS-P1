import requests, json
from functions.rsa import rsa_encrypt, generate_rsa_keys
from functions.aes import generate_aes_key

global server
server = "http://127.0.0.1:5000"

