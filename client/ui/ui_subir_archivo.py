from customtkinter import *
from tkinter import filedialog
from ui.clearApp import clearApp
from functions.encrypt_decrypt import encrypt
# from functions.encrypt_decrypt import encrypt

archivo_path = None

def on_volver(app, user):
    from ui.ui_home import home
    clearApp(app)
    home(app, user)

def seleccionar_archivo():
    global archivo_path #referencio la var global para modificarla

    # Abrir explorador de archivos
    archivo = filedialog.askopenfilename(title="Seleccionar archivo")
    
    if archivo:
        archivo_path = archivo
        # Mostrar texto debajo del botón si el archivo se selecciona
        archivo_subido_label.configure(text=f"Archivo subido correctamente: {archivo.split('/')[-1]}", text_color="green")
        archivo_subido_label.pack(pady=(5, 20))
    else:
        archivo_subido_label.configure(text="No se ha seleccionado ningún archivo", text_color="red")
        archivo_subido_label.pack(pady=(5, 20))

def on_cifrar_archivo(user): 
    # (CODIGO DE EJEMPLO) no controla si se hace correctamente el cifrado
    response = encrypt(archivo_path, user)
    print('si todo va bien el archivo se cifra')
    archivo_cifrado_label.configure(text="Archivo cifrado correctamente", text_color="blue")
    archivo_cifrado_label.pack(pady=(5, 20))


def subir_archivo(app, user):
    # # Crear ventana principal
    # app = CTk()
    # app.geometry("600x400")  # Tamaño de la ventana
    # app.title("Encriptación de Archivos")
    # app.configure(fg_color="white")  # Fondo blanco

    # Título grande centrado en morado
    title_label = CTkLabel(master=app, text="Protege tus archivos", 
                           text_color="#601E88", font=("Arial Bold", 24, "bold"))
    title_label.pack(pady=(40, 5)) 

    # Subtítulo centrado en gris
    subtitle_label = CTkLabel(master=app, text="Sube tus archivos y cífralos aquí", 
                              text_color="#606060", font=("Arial", 15))
    subtitle_label.pack(pady=(5, 40))

    # Botón para "Seleccionar archivo"
    seleccionar_button = CTkButton(master=app, text="Seleccionar archivo", 
                                   fg_color="#601E88", text_color="white", font=("Arial", 14),
                                   hover_color="#D18AF0", corner_radius=32, width=200,
                                   command= seleccionar_archivo)
    seleccionar_button.pack(pady=(5, 20)) 

    # Etiqueta para mostrar el estado del archivo subido (vacía por defecto)
    global archivo_subido_label
    archivo_subido_label = CTkLabel(master=app, text="", 
                                    text_color="green", font=("Arial", 12))


    # Botón para cifrar archivo
    cifrar_button = CTkButton(master=app, text="Cifrar archivo", 
                              fg_color="#601E88", text_color="white", font=("Arial", 14),
                              hover_color="#D18AF0", corner_radius=32,  width=200,
                              command= lambda: on_cifrar_archivo(user))
    cifrar_button.pack(pady=(5, 20))

    # Etiqueta para mostrar si el archivo se ha cifrado bien (vacía por defecto)
    global archivo_cifrado_label
    archivo_cifrado_label = CTkLabel(master=app, text="", 
                                    text_color="green", font=("Arial", 12))

    # Botón volver
    volver_button = CTkButton(master=app, text="Volver", fg_color="#601E88", 
                              text_color="white", font=("Arial", 12), 
                              hover_color="#D18AF0", corner_radius=32, width=20,
                              command=lambda: on_volver(app, user))
    volver_button.place(x=20, y=20)  # Colocar en la parte inferior izquierda

    # Ejecutar la aplicación
    app.mainloop()


