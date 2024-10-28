from pathlib import Path
from customtkinter import *
from CTkMessagebox import CTkMessagebox
from PIL import Image
from ui import ui_registro, ui_home
from ui.clearApp import clearApp
from functions import user_auth
from functions import google_auth
import os


# Función que maneja el evento de inicio de sesión
def on_login(app):
    email = email_var.get()  # Obtener el texto ingresado en el campo de usuario
    password = password_var.get()  # Obtener el texto ingresado en el campo de contraseña
    print(email)
    print(password)
    
    result = user_auth.login(email=email, password=password)
    
    if ( result ):
        clearApp(app) 
        ui_home.home(app= app, user= result)
        

def on_register(app):
    clearApp(app) 
    ui_registro.register_menu(app)

def on_google_login(app):
    resultado = google_auth.google_login()
    
    if (resultado['code'] == '200'):
        successfulLogin(app)
    else:
        CTkMessagebox(title="Error", message="Error al iniciar sesión con Google", icon="cancel")

def login_menu(app):
    # Variables para almacenar los datos introducidos por el usuario
    global email_var, password_var
    email_var = StringVar()
    password_var = StringVar()

    side_img_data = Image.open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), Path('ui/imgs/side-img.png')))
    email_icon_data = Image.open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), Path('ui/imgs/email-icon.png')))
    password_icon_data = Image.open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), Path('ui/imgs/password-icon.png')))
    google_icon_data = Image.open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), Path('ui/imgs/google-icon.png')))

    side_img = CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(300, 480))
    email_icon = CTkImage(dark_image=email_icon_data, light_image=email_icon_data, size=(20,20))
    password_icon = CTkImage(dark_image=password_icon_data, light_image=password_icon_data, size=(17,17))
    google_icon = CTkImage(dark_image=google_icon_data, light_image=google_icon_data, size=(17,17))


    CTkLabel(master=app, text="", image=side_img).pack(expand=True, side="left")
    frame = CTkFrame(master=app, width=300, height=480, fg_color="#ffffff")
    frame.pack_propagate(0)
    frame.pack(expand=True, side="right")

    CTkLabel(master=frame, text="Asegurados", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 24)).pack(anchor="w", pady=(50, 5), padx=(25, 0))
    CTkLabel(master=frame, text="A un solo paso de proteger tus archivos", text_color="#7E7E7E", anchor="w", justify="left", font=("Arial Bold", 12)).pack(anchor="w", padx=(15, 0))

    CTkLabel(master=frame, text="  Email:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14), image=email_icon, compound="left").pack(anchor="w", pady=(38, 0), padx=(25, 0))
    CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000", textvariable=email_var).pack(anchor="w", padx=(25, 0))

    CTkLabel(master=frame, text="  Contraseña:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14), image=password_icon, compound="left").pack(anchor="w", pady=(21, 0), padx=(25, 0))
    CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000", show="*", textvariable=password_var).pack(anchor="w", padx=(25, 0))

    CTkButton(master=frame, text="Iniciar Sesión", fg_color="#601E88", hover_color="#D073F2", font=("Arial Bold", 12), text_color="#ffffff", width=225, command=lambda: on_login(app)).pack(anchor="w", pady=(40, 0), padx=(25, 0))
    CTkButton(master=frame, text="Registrarse", fg_color="#601E88", hover_color="#D073F2", font=("Arial Bold", 12), text_color="#ffffff", width=225, command=lambda: on_register(app)).pack(anchor="w", pady=(10, 0), padx=(25, 0))
    CTkButton(master=frame, text="Continue With Google", fg_color="#EEEEEE", hover_color="#CCCCCC", font=("Arial Bold", 9), text_color="#601E88", width=225, image=google_icon, command=lambda : on_google_login(app)).pack(anchor="w", pady=(20, 0), padx=(25, 0))