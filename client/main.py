import requests, json
from functions.aes import encrypt_file, decrypt_file,generate_aes_key
from functions.rsa import rsa_encrypt, generate_rsa_keys
from customtkinter import CTk, set_appearance_mode
from ui import ui_login, ui_home


# Variables para las peticiciones
global server
server = "http://127.0.0.1:5000"

# Inicializacion de variables para la gestion de interfaces
app = CTk()

app.geometry("600x400")
app.configure(bg="white")
set_appearance_mode("light")

# Llamamos a la interfaz "login" pasandole la app por parametro
# ui_login.login_menu(app)
ui_home.home(app)

app.mainloop()
