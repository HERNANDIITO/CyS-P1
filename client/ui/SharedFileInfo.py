from customtkinter import *
from PIL import Image
from pathlib import Path
import os
import re
import requests
from functions.share_file import share
from functions.consts import server

class SharedInfo(CTkFrame):
    def __init__(self, parent, controller):
        CTkFrame.__init__(self, parent)
        self.controller = controller
        self.fileID = 0  #Id del archivo que se obtiene haciendo reload
        self.usersShared = []  #Listado de usuarios con los que se ha compartido el archivo

        self.emailsWritten = 0
        self.main_frame = CTkFrame(master=self)
        self.main_frame.pack(fill='both')

        # Cargar icono de email
        email_icon_data = Image.open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), Path('ui/imgs/email-icon.png')))
        email_icon = CTkImage(dark_image=email_icon_data, light_image=email_icon_data, size=(20, 20))

        # Cabecera
        header_frame = CTkFrame(self.main_frame, fg_color="transparent")
        header_frame.pack(padx=20, fill="x")

        self.fileName = CTkLabel(
            master=header_frame, 
            text="", 
            font=("Arial", 24, "bold"),
            text_color="#601E88", 
            anchor="w", 
            justify="left"
        )
        self.fileName.pack(side="left", pady=10)


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
        volver_button.pack(side="right", padx=2)

        # Crear tabla justo debajo del subtítulo
        
        self.table_frame = CTkScrollableFrame(self.main_frame, fg_color="white", corner_radius=10, height=125)
        self.table_frame._scrollbar.configure(height=0)

        # Contenedor para el título, email input y botón
        self.email_input_frame = CTkFrame(master=self.main_frame, fg_color="transparent")
        self.email_input_frame.pack(anchor="w", padx=(180, 0))

        # Tabla de emails
        self.email_table = CTkScrollableFrame(master=self.main_frame, fg_color="transparent", width=150, height=125)
        self.email_table.pack(fill='x', padx=20)
        self.email_table._scrollbar.configure(height=0)
        self.emails = []
        
        # Botón de compartir debajo de la tabla de emails
        self.share_button = CTkButton(
            master=header_frame,
            text="Compartir",
            fg_color="#601E88",
            text_color="white",
            font=("Arial", 12),
            hover_color="#D18AF0",
            corner_radius=32,
            width=20,
            command=self.share
        )
        self.share_button.pack(side="right", padx=2)

        subtitle = CTkLabel(
            master=self.email_input_frame,
            text="Compartir con más personas:",
            text_color="#6B6B6B",
            font=("Arial", 14)
        )
        subtitle.pack(anchor="w")
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
        email_label.pack(anchor="w")

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
            master=self.main_frame,
            text="El archivo está compartido con:",
            text_color="#6B6B6B",
            font=("Arial", 14),
        )
        subtitle.pack(pady=(0, 10))
        self.error_label = CTkLabel(master=self, text="", text_color="red", font=("Arial", 12))
        self.error_label.pack()


    def create_user_table(self):
        """Crea una tabla con datos de usuarios con los que se ha compartido el archivo."""
        self.table_frame.pack_forget()

        # Eliminar todas las filas existentes en la tabla
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        # Cabecera de la tabla
        header = CTkFrame(self.table_frame, fg_color="#601E88")
        header.pack(fill="x")
        CTkLabel(header, text="Nombre", text_color="white", width=15).pack(side="left", padx=10)
        CTkLabel(header, text="Email", text_color="white", width=20).pack(side="left", padx=10)
        CTkLabel(header, text="Acción", text_color="white", width=10).pack(side="right", padx=10)

        # Filas de la tabla
        for user in self.usersShared:
            row = CTkFrame(self.table_frame, fg_color="#EEEEEE")
            row.pack(fill="x")
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
        
        self.table_frame.pack(fill="x", padx=20)


    def remove_user(self, user):
        """Lógica para eliminar un usuario de la tabla."""
        print(f"Usuario eliminado: {user}")
        user_email = user["email"]  # Cambiar por la clave adecuada
        file_id = self.fileID       # Cambiar por el valor adecuado

        # Crear el body de la solicitud
        body = {
            "reciever_email": user_email,
            "file_id": file_id
        }

        # Realizar la solicitud DELETE con datos en el body
        r = requests.delete(f"{server}/shared-user", json=body)

        # Manejo de la respuesta
        if r.status_code == 200:
            print("Usuario compartido eliminado con éxito:", r.json())
        else:
            print(f"Error al eliminar usuario compartido: {r.status_code}, {r.text}")

        self.reload(self.fileID)


    #Comprobar que el email introducido es correcto y en tal caso se añade a la tabla de emails
    def validate_and_add_email(self):
        email = self.email_entry.get().strip()
        if self.is_valid_email(email):
            self.add_email_to_table(email)
            self.error_label.configure(text="")
            self.email_entry.delete(0, "end") 
            self.emailsWritten += 1 
            self.show_share_button()
        else:
            self.error_label.configure(text="Email no válido")
    
    #Validar que el formato del email es válido
    def is_valid_email(self, email):
        return re.match(r"[^@]+@[^@]+", email) is not None
    
    #Añadir email a la tabla
    def add_email_to_table(self, email):
        if email not in self.emails:
            self.emails.append(email)
            
            email_mostrado = email
            if len(email) > 15:
                email_mostrado = email[:12] + "..." #En caso de tener una longitud mayor a 15 caracteres, tan solo se muestran ls 12 primeros
            
            row_frame = CTkFrame(master=self.email_table, fg_color="#FFFFFF")
            row_frame.pack(fill="x")
            
            # Configuramos el grid del row_frame para ocupar dos columnas
            row_frame.columnconfigure(0, weight=1)  # Para que la primera columna se expanda
            row_frame.columnconfigure(1, weight=0)  # La segunda columna no se expande
            
            # Label para el email
            row = CTkLabel(
                master=row_frame,
                text=email_mostrado,
                text_color="#000000",
                anchor="w",
                font=("Arial", 12),
                fg_color="#FFFFFF",
                width=75
            )
            row.grid(row=0, column=0, padx=(5, 15), sticky="w")

            # Botón para eliminar email
            add_remove_email = CTkButton(
                master=row_frame,
                text="-",
                fg_color="#601E88",
                hover_color="#D18AF0",
                text_color="#ffffff",
                width=25,
                command=lambda: self.remove_email_of_table(row_frame, email)
            )
            add_remove_email.grid(row=0, column=1, sticky="e")

    
    #Quitar email de la tabla
    def remove_email_of_table(self, row_frame, email):
        if email in self.emails:
            self.emails.remove(email)
            self.emailsWritten -= 1
            self.show_share_button()
        
        row_frame.destroy()

    #Mostrar botón de compartir
    def show_share_button(self):
        if self.emailsWritten > 0: 
            self.share_button.pack()
            self.share_button.configure(state="normal")
        else:
            self.share_button.configure(state="disabled")   #En caso de quitar emails y quedarse la tabla a 0 emails, desabilitar el botón
            print(self.emailsWritten)

    def on_volver(self):
        self.controller.show_frame("Home")

    #Compartir archivo con los emails especificados
    def share(self):
        for email in self.emails :
            r = requests.get(f"{server}/users/shareParamsByEmail/{email}")
            print(r)
            r = r.json()
            print(r)
            
            if (str(r['code']) == "200"):
                print("sharing!", r)
                result = share(sharedFileId = self.fileID, recieverId = r['body']['userID'], transmitter = self.controller.user, recieverPublicRSAKey = r['body']['publicRSA'], AESKey = self.fileJSON['body']['aesKey'])
                print("sharing result: ", result)
                self.reload(self.fileID)



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

        print(self.usersShared)
        self.create_user_table()
