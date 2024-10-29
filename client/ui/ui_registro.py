from pathlib import Path
from customtkinter import *
from PIL import Image
from functions import user_auth
from functions.rsa import generate_rsa_keys
from ui import ui_home, ui_login
from ui.clearApp import clearApp
import os
import requests, json

# LA LINEA 43 NO VA


global server
server = "http://127.0.0.1:5000"

# Todo ha sido hecho sin ayuda de ChatGPT, tened huevos a acribillarme ahora SIUUUUUUU

def on_register(app):

    username = username_var.get()
    password = password_var.get()
    pass2 = pass2_var.get()
    email = email_var.get()

    user = user_auth.register(username, email, password, pass2)
    print("user:", user)

    if(user):
        clearApp(app)
        ui_home.home(app, user)

def on_login(app):
    clearApp(app)
        
    ui_login.login_menu(app)


def register_menu(app):
    # Variables para almacenar los datos introducidos por el usuario
    global username_var, password_var, pass2_var, email_var
    username_var = StringVar()
    password_var = StringVar()
    pass2_var = StringVar()
    email_var = StringVar()

    side_img_data = Image.open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), Path('ui/imgs/side-img.png')))
    email_icon_data = Image.open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), Path('ui/imgs/email-icon.png')))
    password_icon_data = Image.open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), Path('ui/imgs/password-icon.png')))
    google_icon_data = Image.open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), Path('ui/imgs/google-icon.png')))
    user_icon_data = Image.open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), Path('ui/imgs/user_icon.png')))

    side_img = CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(300, 480))
    email_icon = CTkImage(dark_image=email_icon_data, light_image=email_icon_data, size=(20,20))
    password_icon = CTkImage(dark_image=password_icon_data, light_image=password_icon_data, size=(17,17))
    google_icon = CTkImage(dark_image=google_icon_data, light_image=google_icon_data, size=(17,17))
    user_icon = CTkImage(dark_image=user_icon_data, light_image=user_icon_data, size=(17,17))

    CTkLabel(master=app, text="", image=side_img).pack(expand=True, side="left")

    frame = CTkFrame(master=app, width=300, height=480, fg_color="#ffffff")
    frame.pack_propagate(0)
    frame.pack(expand=True, side="right")

    CTkLabel(master=frame, text="Asegurados", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 24)).pack(anchor="w", pady=(20, 5), padx=(25, 0))
    CTkLabel(master=frame, text="Registrate para proteger tus archivos", text_color="#7E7E7E", anchor="w", justify="left", font=("Arial Bold", 12)).pack(anchor="w", padx=(15, 0))

    CTkLabel(master=frame, text="  Usuario:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14), image=user_icon, compound="left").pack(anchor="w", pady=(20, 0), padx=(25, 0))
    CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000", textvariable=username_var).pack(anchor="w", padx=(25, 0))

    CTkLabel(master=frame, text="  Contraseña:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14), image=password_icon, compound="left").pack(anchor="w", pady=(10, 0), padx=(25, 0))
    CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000", show="*", textvariable=password_var).pack(anchor="w", padx=(25, 0))

    CTkLabel(master=frame, text="  Confirmar contraseña:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14), image=password_icon, compound="left").pack(anchor="w", pady=(10, 0), padx=(25, 0))
    CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000", show="*", textvariable=pass2_var).pack(anchor="w", padx=(25, 0))

    CTkLabel(master=frame, text="  Email:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14), image=email_icon, compound="left").pack(anchor="w", pady=(10, 0), padx=(25, 0))
    CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000", textvariable=email_var).pack(anchor="w", padx=(25, 0))
    
    CTkButton(master=frame, text="Registrarse", fg_color="#601E88", hover_color="#D073F2", font=("Arial Bold", 12), text_color="#ffffff", width=225, command= lambda : on_register(app)).pack(anchor="w", pady=(15, 0), padx=(25, 0))
    CTkButton(master=frame, text="Iniciar sesión", fg_color="#601E88", hover_color="#D073F2", font=("Arial Bold", 12), text_color="#ffffff", width=225, command= lambda : on_login(app)).pack(anchor="w", pady=(10, 0), padx=(25, 0))
    CTkButton(master=frame, text="Continue With Google", fg_color="#EEEEEE", hover_color="#CCCCCC", font=("Arial Bold", 9), text_color="#601E88", width=225, image=google_icon).pack(anchor="w", pady=(10, 0), padx=(25, 0))