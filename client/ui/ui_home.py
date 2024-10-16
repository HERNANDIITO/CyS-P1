from customtkinter import *
from CTkTable import CTkTable
from ui.ui_subir_archivo import subir_archivo

def home(app):

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
        command = lambda : subir_archivo(app)
    )

    btn_selec_archivo.pack(side="right")

    subtitle = CTkLabel(master=app, text="Estos son tus archivos:", text_color="#6B6B6B", font=("Arial", 14))
    subtitle.pack(pady=(20,0))

    table_data = [
        ["ID", "Nombre de archivo", "Tamaño"],
        ['3833', 'Smartphone', 'Alice'],
        ['6432', 'Laptop', 'Bob'],
        ['2180', 'Tablet', 'Crystal'],
        ['5438', 'Headphones', 'John'],
    ]


    table = CTkTable(master=app, values=table_data, colors=["#FFFFFF", "#FFFFFF"], 
                    header_color="purple", hover_color="#EEEEEE")

    table.edit_row(0, text_color="#FFFFFF", hover_color="purple")

    table.pack(expand=True)