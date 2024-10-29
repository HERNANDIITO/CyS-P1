from customtkinter import *
from CTkTable import CTkTable
from ui.clearApp import clearApp
from ui.ui_subir_archivo import subir_archivo
from functions.file_requests import download_file

def on_subir_archivo(app, user):
    clearApp(app)
    subir_archivo(app, user)

def on_button_click(row_id):
    print(f"Botón de la fila {row_id} presionado")

def home(app, user):

    # Frame para colocar el título y el botón en la misma línea 
    # (Idea de ChatGPT pero he entendido lo que ha puesto y he modificado cosas, no me acribilleis por favor, os puedo explicar todo el código si hace falta)
    header_frame = CTkFrame(master=app, fg_color="transparent")
    header_frame.pack(pady=(30, 20), padx=20, fill="x")


    title = CTkLabel(master=header_frame, text="Página principal", font=("Arial", 24), 
                    text_color="purple", anchor="w", justify="left")
    title.pack(side="left")

    btn_selec_archivo = CTkButton(
        master = header_frame,
        text = "Ir a subir archivo",
        corner_radius = 32, 
        fg_color = "purple",
        hover_color = "#A16FB0",
        text_color = "#ffffff",
        command = lambda : on_subir_archivo(app, user)
    )

    btn_selec_archivo.pack(side="right")

    subtitle = CTkLabel(master=app, text="Estos son tus archivos:", text_color="#6B6B6B", font=("Arial", 14))
    subtitle.pack(pady=(20,50))

    table_data = [
        ["ID", "Nombre de archivo", "Tamaño"],
        ['1', 'Smartphone', 'Alice'],
        ['6432', 'Laptop', 'Bob'],
        ['2180', 'Tablet', 'Crystal'],
        ['5438', 'Headphones', 'John'],
    ]

    # Crear las filas manualmente con botones a la derecha
    for idx, row in enumerate(table_data):
        # Establecer el marco de la fila
        if idx == 0:
            row_frame = CTkFrame(master=app, fg_color="purple", border_color="purple", border_width=2)
            row_frame.pack(fill="x", padx=20, pady=5)
        else:
            row_frame = CTkFrame(master=app, fg_color="#FFFFFF")
            row_frame.pack(fill="x", padx=20, pady=5)

        # Añadir celdas a la fila
        for cell_idx, cell in enumerate(row):  # Usa enumerate para obtener el índice de la celda
            # Si es la primera fila
            if idx == 0:
                cell_label = CTkLabel(master=row_frame, text=cell, text_color="#FFFFFF", anchor="w", width=100)
                cell_label.pack(side="left", padx=10)
            else:
                cell_label = CTkLabel(master=row_frame, text=cell, anchor="w", width=100)
                cell_label.pack(side="left", padx=10)

        # Añadir el botón a la derecha
        if idx != 0:
            btn_action = CTkButton(
                master=row_frame, 
                text="Descargar",
                corner_radius=32, 
                fg_color="purple",
                hover_color="#A16FB0",
                text_color="#ffffff",
                command= lambda : download_file(0)
            )
            btn_action.pack(side="right", padx=(10, 0))
