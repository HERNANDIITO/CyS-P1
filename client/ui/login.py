from pathlib import Path
from customtkinter import *
from PIL import Image
from functions.user import User
from functions import user_auth, debug
import threading, queue

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

        side_img = CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(300, 480))
        email_icon = CTkImage(dark_image=email_icon_data, light_image=email_icon_data, size=(20,20))
        password_icon = CTkImage(dark_image=password_icon_data, light_image=password_icon_data, size=(17,17))

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
              
    def successfullLogin(self, user: User):
        dialog = CTkInputDialog(text="Escribe tu código de doble factor de autenticación:", title="Código OTP")
        otp_code = dialog.get_input()

        result_queue = queue.Queue()
        hilo = threading.Thread(target=user_auth.check2fa, args=(user, otp_code, result_queue))
        hilo.daemon = True  # Asegura que el hilo se cierre al cerrar la app
        hilo.start()
        hilo.join()
        result = result_queue.get()
        
        if ( type(result) is User ):
            self.controller.user = user
            self.controller.load_restricted_frames()
            print(debug.printMoment(), "mostrando home...")
            self.controller.show_frame("Home")
        else:
            self.controller.show_error("Código OTP incorrecto")

    # Función que maneja el evento de inicio de sesión
    def on_login(self):
        password = self.password_var.get()  # Obtener el texto ingresado en el campo de contraseña
        email = self.email_var.get()  # Obtener el texto ingresado en el campo de usuario
        
        print(debug.printMoment(), "Iniciando login...")
        result_queue = queue.Queue()
        hilo = threading.Thread(target=user_auth.login, args=(email, password, result_queue))
        hilo.daemon = True  # Asegura que el hilo se cierre al cerrar la app
        hilo.start()
        hilo.join()
        result = result_queue.get()
        print(debug.printMoment(), "Loggin terminado...")
        
        if ( type(result) is User ):
            self.successfullLogin(user=result)
        else:
            self.controller.show_error(result.msg)

    def on_register(self):
        self.controller.show_frame("Register")