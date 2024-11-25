from pathlib import Path
from customtkinter import *
from CTkMessagebox import CTkMessagebox
from PIL import Image
from functions import user_auth
from functions import google_auth

import os

class Login(CTkFrame):
    def __init__(self, parent, controller):
        CTkFrame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        # Variables para almacenar los datos introducidos por el usuario
        self.email_var = StringVar()
        self.password_var = StringVar()

        side_img_data = Image.open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), Path('ui/imgs/side-img.png')))
        email_icon_data = Image.open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), Path('ui/imgs/email-icon.png')))
        password_icon_data = Image.open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), Path('ui/imgs/password-icon.png')))
        google_icon_data = Image.open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), Path('ui/imgs/google-icon.png')))

        side_img = CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(300, 480))
        email_icon = CTkImage(dark_image=email_icon_data, light_image=email_icon_data, size=(20,20))
        password_icon = CTkImage(dark_image=password_icon_data, light_image=password_icon_data, size=(17,17))
        google_icon = CTkImage(dark_image=google_icon_data, light_image=google_icon_data, size=(17,17))

        CTkLabel(master=self, text="", image=side_img).pack(expand=True, side="left")
        frame = CTkFrame(master=self, width=300, height=480, fg_color="#ffffff")
        frame.pack_propagate(0)
        frame.pack(expand=True, side="right")

        CTkLabel(master=frame, text="Asegurados", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 24, "bold")).pack(anchor="w", pady=(50, 5), padx=(25, 0))
        CTkLabel(master=frame, text="A un solo paso de proteger tus archivos", text_color="#7E7E7E", anchor="w", justify="left", font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 0))

        CTkLabel(master=frame, text="  Email:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14), image=email_icon, compound="left").pack(anchor="w", pady=(38, 0), padx=(25, 0))
        CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000", corner_radius = 32, textvariable=self.email_var).pack(anchor="w", padx=(25, 0))

        CTkLabel(master=frame, text="  Contraseña:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14), image=password_icon, compound="left").pack(anchor="w", pady=(21, 0), padx=(25, 0))
        CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000", show="*", corner_radius = 32, textvariable=self.password_var).pack(anchor="w", padx=(25, 0))

        CTkButton(master=frame, text="Iniciar Sesión", fg_color="#601E88", hover_color="#D18AF0", font=("Arial Bold", 12), text_color="#ffffff", corner_radius = 32, width=225, command=self.on_login).pack(anchor="w", pady=(40, 0), padx=(25, 0))
        CTkButton(master=frame, text="Registrarse", fg_color="#9674AC", hover_color="#D18AF0", font=("Arial Bold", 12), text_color="#ffffff", corner_radius = 32, width=225, command=self.on_register).pack(anchor="w", pady=(10, 0), padx=(25, 0))
        CTkButton(master=frame, text="Continuar con Google", fg_color="#EEEEEE", hover_color="#CCCCCC", font=("Arial Bold", 9), text_color="#601E88", corner_radius = 32, width=225, image=google_icon, command=lambda : self.on_google_login()).pack(anchor="w", pady=(20, 0), padx=(25, 0))
              
    def successfullLogin(self, user):
        self.controller.user = user
        self.controller.load_restricted_frames()
        self.controller.show_frame("Home")


    # Función que maneja el evento de inicio de sesión
    def on_login(self):
        password = self.password_var.get()  # Obtener el texto ingresado en el campo de contraseña
        email = self.email_var.get()  # Obtener el texto ingresado en el campo de usuario
        
        result = user_auth.login(email=email, password=password)
        
        if ( result ):
            self.successfullLogin(user=result)
            
    def on_google_login(self):
        resultado = google_auth.google_login()
        
        if (resultado):
            self.successfullLogin(user = resultado)
        else:
            CTkMessagebox(title="Error", message="Error al iniciar sesión con Google", icon="cancel")

    def on_register(self):
        self.controller.show_frame("Register")