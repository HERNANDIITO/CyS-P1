import requests, json
from functions.aes import encrypt_file, decrypt_file,generate_aes_key
from functions.rsa import rsa_encrypt, generate_rsa_keys
from customtkinter import CTk, set_appearance_mode
from ui import ui_login
from ui import ui_registro
from functions.user_auth import register, login


# Variables para las peticiciones
global server
server = "http://127.0.0.1:5000"

# Inicializacion de variables para la gestion de interfaces
app = CTk()

# app.geometry("600x480")     # Tamaño de la ventana de la app modificado, antes era (600x400), dicha modificación está hecha para adaptar la ventana al tamaño de la imagen
# app.configure(bg="white")
# set_appearance_mode("light")

# Llamamos a la interfaz "login" pasandole la app por parametro
# ui_login.login_menu(app)
ui_registro.register_menu(app)

# register(email="g@gamil.com", password="12345678", password2="12345678", username="AAAA" )
# login(email="g@gamil.com", password="12345678")


# japp.mainloop()
