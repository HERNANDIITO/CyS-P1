from pathlib import Path
from customtkinter import *
from PIL import Image
from functions import user_auth
from functions.user import User
import os

# LA LINEA 43 NO VA
# Todo ha sido hecho sin ayuda de ChatGPT, tened huevos a acribillarme ahora SIUUUUUUU

class Register(CTkFrame):
    def __init__(self, parent, controller):
        CTkFrame.__init__(self, parent)
        self.controller = controller
        
        # Variables para almacenar los datos introducidos por el usuario
        self.username_var = StringVar()
        self.password_var = StringVar()
        self.pass2_var = StringVar()
        self.email_var = StringVar()

        side_img_data = Image.open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), Path('ui/imgs/side-img.png')))
        email_icon_data = Image.open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), Path('ui/imgs/email-icon.png')))
        password_icon_data = Image.open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), Path('ui/imgs/password-icon.png')))
        user_icon_data = Image.open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), Path('ui/imgs/user_icon.png')))

        side_img = CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(300, 480))
        email_icon = CTkImage(dark_image=email_icon_data, light_image=email_icon_data, size=(20,20))
        password_icon = CTkImage(dark_image=password_icon_data, light_image=password_icon_data, size=(17,17))
        user_icon = CTkImage(dark_image=user_icon_data, light_image=user_icon_data, size=(17,17))

        CTkLabel(master=self, text="", image=side_img).pack(expand=True, side="left")

        frame = CTkFrame(master=self, width=300, height=480, fg_color="#ffffff")
        frame.pack_propagate(0)
        frame.pack(expand=True, side="right")

        CTkLabel(master=frame, text="Asegurados", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 24, "bold")).pack(anchor="w", pady=(20, 5), padx=(25, 0))
        CTkLabel(master=frame, text="Regístrate para proteger tus archivos", text_color="#7E7E7E", anchor="w", justify="left", font=("Arial Bold", 12)).pack(anchor="w", padx=(25, 0))

        CTkLabel(master=frame, text="  Usuario:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14), image=user_icon, compound="left").pack(anchor="w", pady=(20, 0), padx=(25, 0))
        CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, corner_radius = 32, text_color="#000000", textvariable=self.username_var).pack(anchor="w", padx=(25, 0))

        CTkLabel(master=frame, text="  Contraseña:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14), image=password_icon, compound="left").pack(anchor="w", pady=(10, 0), padx=(25, 0))
        CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, corner_radius = 32, text_color="#000000", show="*", textvariable=self.password_var).pack(anchor="w", padx=(25, 0))

        CTkLabel(master=frame, text="  Confirmar contraseña:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14), image=password_icon, compound="left").pack(anchor="w", pady=(10, 0), padx=(25, 0))
        CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, corner_radius = 32, text_color="#000000", show="*", textvariable=self.pass2_var).pack(anchor="w", padx=(25, 0))

        CTkLabel(master=frame, text="  Email:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 14), image=email_icon, compound="left").pack(anchor="w", pady=(10, 0), padx=(25, 0))
        CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, corner_radius = 32, text_color="#000000", textvariable=self.email_var).pack(anchor="w", padx=(25, 0))
        
        CTkButton(master=frame, text="Registrarse", fg_color="#601E88", hover_color="#D18AF0", font=("Arial Bold", 12), text_color="#ffffff", corner_radius = 32, width=225, command=self.on_register).pack(anchor="w", pady=(15, 0), padx=(25, 0))
        CTkButton(master=frame, text="Iniciar sesión", fg_color="#9674AC", hover_color="#D18AF0", font=("Arial Bold", 12), text_color="#ffffff", corner_radius = 32, width=225, command= self.on_login).pack(anchor="w", pady=(10, 0), padx=(25, 0))

    def on_register(self):
        username    = self.username_var.get()
        password    = self.password_var.get()
        pass2       = self.pass2_var.get()
        email       = self.email_var.get()

        result = user_auth.register(username, email, password, pass2)

        if(type(result) is User):
            self.controller.user = result
            self.controller.load_restricted_frames()
            self.controller.show_frame("OtpQrCode")
        else:
            self.controller.show_error(result.msg)

    def on_login(self):
        self.controller.show_frame("Login")