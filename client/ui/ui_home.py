import requests
from customtkinter import *
from ui.clearApp import clearApp
from ui.ui_subir_archivo import subir_archivo
from functions.file_requests import download_file
from functions.encrypt_decrypt import decrypt

def on_subir_archivo(app):
    clearApp(app)
    subir_archivo(app)

def home(app, user):

    # Realiza una solicitud GET al servidor para obtener los archivos del usuario
    try:
        response = requests.get(f'http://localhost:5000/files/{user.userId}')
        response.raise_for_status()
        archivos = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener archivos: {e}")
        return

    # Estructura de la interfaz gráfica
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
        command = lambda : on_subir_archivo(app)
    )

    btn_selec_archivo.pack(side="right")

    subtitle = CTkLabel(master=app, text="Estos son tus archivos:", text_color="#6B6B6B", font=("Arial", 14))
    subtitle.pack(pady=(20, 50))

    # Inicializar la tabla de datos con encabezados
    table_data = [
        ["ID", "Nombre de archivo"]
    ]

    # Comprueba que el usuario tenga al menos un fichero
    if (archivos["body"]):
        # Rellenar la tabla con los datos obtenidos de la respuesta del servidor
        for archivo in archivos["body"]["files"]:
            archivo_id = archivo["fileId"]
            nombre_archivo = archivo["fileName"]
            table_data.append([archivo_id, nombre_archivo])

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
        for cell in row:
            text_color = "#FFFFFF" if idx == 0 else "#000000"
            cell_label = CTkLabel(master=row_frame, text=cell, text_color=text_color, anchor="w", width=100)
            cell_label.pack(side="left", padx=10)

        # Añadir el botón de descarga a la derecha si no es la fila de encabezado
        if idx != 0:
            btn_action = CTkButton(
                master=row_frame,
                text="Descargar",
                corner_radius=32,
                fg_color="purple",
                hover_color="#A16FB0",
                text_color="#ffffff",
                command=lambda archivo_id=row[0], nombre_archivo=row[1]: procesar_guardado(archivo_id, nombre_archivo)  # Pasa el ID del archivo al botón
            )
            btn_action.pack(side="right", padx=(10, 0))
        
def procesar_guardado(archivo_id, nombre_archivo):
    download_file(archivo_id, nombre_archivo)

    decrypt(nombre_archivo)