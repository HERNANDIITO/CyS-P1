from customtkinter import *
from PIL import Image
from pathlib import Path
import os
import re
import requests

global server
server = "http://127.0.0.1:5000"

class SharedInfo(CTkFrame):
    def __init__(self, parent, controller):
        CTkFrame.__init__(self, parent)
        self.controller = controller
        self.fileID = 0  #el id del archivo que obtendremos haciendo reload
        self.usersShared = []  #el listado de usuarios con los que se ha compartido el archivo que lo obtendremos haciendo reload

        self.geometry = "600x480"  # Estableciendo las dimensiones
        self.title = "Asegurados"

        # Cargar icono de email
        email_icon_data = Image.open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), Path('ui/imgs/email-icon.png')))
        email_icon = CTkImage(dark_image=email_icon_data, light_image=email_icon_data, size=(20, 20))


        # Cabecera
        header_frame = CTkFrame(self, fg_color="transparent")
        header_frame.pack(pady=(30, 20), padx=20, fill="x")

        self.fileName = CTkLabel(
            master=header_frame, 
            text="", 
            font=("Arial", 24, "bold"),
            text_color="#601E88", 
            anchor="w", 
            justify="left"
        )
        self.fileName.pack(side="left")


        # Botón volver
        volver_button = CTkButton(
            master=header_frame,
            text="Volver",
            fg_color="#601E88",
            text_color="white",
            font=("Arial", 12),
            hover_color="#D18AF0",
            corner_radius=32,
            width=20,
            command=self.on_volver
        )
        volver_button.pack(side="right", padx=(0, 0), pady=10)

        # Contenedor para el título, email input y botón
        self.email_input_frame = CTkFrame(master=self, fg_color="transparent")
        self.email_input_frame.pack(anchor="w", pady=(10, 20), padx=(180, 0))

        

        # Crear tabla justo debajo del subtítulo
        self.table_frame = CTkScrollableFrame(self, fg_color="white", corner_radius=10)
        # self.create_user_table(self.email_input_frame)

        subtitle = CTkLabel(
            master=self.email_input_frame,
            text="Compartir con más personas:",
            text_color="#6B6B6B",
            font=("Arial", 14)
        )
        subtitle.pack(anchor="w", pady=(20, 10))

        # Resto de componentes (input, botón, etc.)
        email_label = CTkLabel(
            master=self.email_input_frame,
            text="  Email:",
            text_color="#601E88",
            anchor="w",
            justify="left",
            font=("Arial Bold", 14),
            image=email_icon,
            compound="left"
        )
        email_label.pack(anchor="w", pady=(0, 5))

        self.email_entry = CTkEntry(
            master=self.email_input_frame,
            width=225,
            fg_color="#EEEEEE",
            border_color="#601E88",
            border_width=1,
            text_color="#000000",
            corner_radius=32
        )
        self.email_entry.pack(side="left", padx=(0, 10))

        add_email_button = CTkButton(
            master=self.email_input_frame,
            text="+",
            command=self.validate_and_add_email,
            fg_color="#601E88",
            hover_color="#D18AF0",
            text_color="#ffffff",
            width=25
        )
        add_email_button.pack(side="left")

        # Subtítulos dentro del frame
        subtitle = CTkLabel(
            master=self,
            text="El archivo está compartido con:",
            text_color="#6B6B6B",
            font=("Arial", 14),
        )
        subtitle.pack(pady=(10, 10))

        self.error_label = CTkLabel(master=self, text="", text_color="red", font=("Arial", 12))
        self.error_label.pack(pady=(10, 0))

        

















    

    def create_user_table(self):
        """Crea una tabla con datos de usuarios con los que se ha compartido el archivo."""
        self.table_frame = CTkFrame(self, fg_color="white", corner_radius=10)
        self.table_frame.pack(fill="x", padx=20, pady=(10, 20))

        # Cabecera de la tabla
        header = CTkFrame(self.table_frame, fg_color="#601E88")
        header.pack(fill="x", pady=(0, 5))
        CTkLabel(header, text="Nombre", text_color="white", width=15).pack(side="left", padx=10)
        CTkLabel(header, text="Email", text_color="white", width=20).pack(side="left", padx=10)
        CTkLabel(header, text="Acción", text_color="white", width=10).pack(side="right", padx=10)

        # Datos ficticios
        users = [
            {"name": "Juan Pérez", "email": "juan.perez@example.com"},
            {"name": "Ana López", "email": "ana.lopez@example.com"},
            {"name": "Carlos García", "email": "carlos.garcia@example.com"}
        ]

    
        def truncate_with_ellipsis(value, max_length):
            if len(value) > max_length:
                return value[:max_length] + "..."
            return value


        max_length = 15
        transformed_users = [
            {
                "name": truncate_with_ellipsis(user["name"], max_length),
                "email": truncate_with_ellipsis(user["email"], max_length)
            }
            for user in self.usersShared
        ]

        # Filas de la tabla
        for user in transformed_users:
            row = CTkFrame(self.table_frame, fg_color="#EEEEEE")
            row.pack(fill="x", pady=2)
            CTkLabel(row, text=user["name"], text_color="#000000", width=15).pack(side="left", padx=10)
            CTkLabel(row, text=user["email"], text_color="#000000", width=20).pack(side="left", padx=10)
            CTkButton(
                row,
                text="Eliminar",
                fg_color="#D9534F",
                hover_color="#C9302C",
                text_color="white",
                width=10,
                command=lambda u=user: self.remove_user(u)
            ).pack(side="right", padx=10)




    def remove_user(self, user):
        """Lógica para eliminar un usuario de la tabla."""
        print(f"Usuario eliminado: {user}")


    def validate_and_add_email(self):
        email = self.email_entry.get().strip()
        if self.is_valid_email(email):
            self.add_email_to_table(email)
            self.error_label.configure(text="")
            self.email_entry.delete(0, "end") 
            self.patata = 1 
            self.show_share_button()
        else:
            self.error_label.configure(text="Email no válido")
    
    def is_valid_email(self, email):
        return re.match(r"[^@]+@[^@]+", email) is not None
    
    def add_email_to_table(self, email):
        if email not in self.emails:
            self.emails.append(email)
            row = CTkLabel(
                master=self.email_table,
                text=email,
                text_color="#000000",
                anchor="center",
                font=("Arial", 12),
                fg_color="#FFFFFF",
                width = 100
            )
            row.pack(fill="x", pady=0, padx=180)

    def show_share_button(self):
        if self.patata == 1: 
            self.share_button.pack(pady=(20, 10), padx=(250, 0))

    def on_volver(self):
        self.controller.show_frame("Home")

    def on_dejar_de_compartir(self):
        self.controller.show_frame("Home")

    def reload(self, fileID):
        self.fileID = fileID
        r = requests.get(f"{server}/get-file-info/{self.fileID}")
        self.fileJSON = r.json()
        self.fileName.configure(text=f"Informacion del archivo: { self.fileJSON['body']["fileName"] + self.fileJSON['body']["fileType"] }" )
 



        req = requests.get(f"{server}/users-shared-to/{self.fileID}")
        print(req)
        self.usersSharedJSON = req.json()
        print(self.usersSharedJSON['body'])

        # Obtén la lista de usuarios desde el JSON
        users_data = self.usersSharedJSON.get('body', {}).get('users', [])
        for user in users_data:
            print(user["user"])

        self.usersShared = []
        
        # Transforma los datos al formato deseado
        for user in users_data:
            newUser = {"name": user["user"], "email": user["email"]}
            self.usersShared.append(newUser)
            
        


        # self.usersShared = [
        #     for user in users_data:
        #         {"name": user["user"], "email": user["email"]}
        # ]
        print(self.usersShared)
        self.create_user_table()




