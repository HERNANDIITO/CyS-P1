from customtkinter import *
from PIL import Image
from pathlib import Path
import os
import re

class Share(CTkFrame):
    def __init__(self, parent, controller):
        CTkFrame.__init__(self, parent)
        self.controller = controller
        
        self.patata = 0 
        
        # Cargar icono de email
        email_icon_data = Image.open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), Path('ui/imgs/email-icon.png')))
        email_icon = CTkImage(dark_image=email_icon_data, light_image=email_icon_data, size=(20, 20))
        
        # Configurar scroll
        self.canvas = CTkCanvas(self, bg="#DBDBDB", highlightthickness=0, width=0)
        self.scrollbar = CTkScrollbar(self, orientation="vertical", command=self.canvas.yview)
        self.scrollable_frame = CTkFrame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Cabecera
        header_frame = CTkFrame(self.scrollable_frame, fg_color="transparent")
        header_frame.pack(pady=(30, 20), padx=20, fill="x")
        
        title = CTkLabel(master=header_frame, text="Compartir archivo", font=("Arial", 24, "bold"), 
                         text_color="#601E88", anchor="w", justify="left")
        title.pack(side="left")

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
        volver_button.pack(side="right", padx=(275, 0), pady=10)
 

        # Contenedor para el título, email input y botón
        email_input_frame = CTkFrame(master=self.scrollable_frame, fg_color="transparent")
        email_input_frame.pack(anchor="w", pady=(10, 20), padx=(180, 0))

        # Subtítulos dentro del frame
        subtitle = CTkLabel(
            master=email_input_frame,
            text="El archivo a compartir es:",
            text_color="#6B6B6B",
            font=("Arial", 14)
        )
        subtitle.pack(anchor="w", pady=(0, 10))

        subtitle = CTkLabel(
            master=email_input_frame,
            text="Compartir con:",
            text_color="#6B6B6B",
            font=("Arial", 14)
        )
        subtitle.pack(anchor="w", pady=(0, 10))

        # Icono y etiqueta de email dentro del frame
        email_label = CTkLabel(
            master=email_input_frame,
            text="  Email:",
            text_color="#601E88",
            anchor="w",
            justify="left",
            font=("Arial Bold", 14),
            image=email_icon,
            compound="left"
        )
        email_label.pack(anchor="w", pady=(0, 5))

        # Input de email
        self.email_entry = CTkEntry(
            master=email_input_frame,
            width=225,
            fg_color="#EEEEEE",
            border_color="#601E88",
            border_width=1,
            text_color="#000000",
            corner_radius=32
        )
        self.email_entry.pack(side="left", padx=(0, 10))

        # Botón para agregar email
        add_email_button = CTkButton(
            master=email_input_frame,
            text="+",
            command=self.validate_and_add_email,
            fg_color="#601E88",
            hover_color="#D18AF0",
            text_color="#ffffff",
            width = 25
        )
        add_email_button.pack(side="left")

        
        # Mensaje de error
        self.error_label = CTkLabel(master=self.scrollable_frame, text="", text_color="red", font=("Arial", 12))
        self.error_label.pack(pady=(0, 0))
        
        # Tabla de emails
        self.email_table = CTkFrame(master=self.scrollable_frame, fg_color="transparent")
        self.email_table.pack(fill="both", expand=True, padx=20, pady=10)
        self.emails = []

        # Botón de compartir debajo de la tabla de emails
        self.share_button = CTkButton(
            master=self.scrollable_frame,
            text="Compartir",
            fg_color="#601E88",
            hover_color="#D18AF0",
            text_color="#ffffff",
            width=100,
            state="normal"
        )
        self.share_button.pack_forget()


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
