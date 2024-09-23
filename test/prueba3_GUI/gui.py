# https://www.youtube.com/watch?v=q8WDvrjPt0M

# import tkinter as tk
# from tkinter import filedialog

# ruta_archivo = None

# # Función que se ejecuta cuando se presiona el botón
# def seleccionar_archivo():
#     # Abrir un cuadro de diálogo para seleccionar el archivo
#     ruta_archivo = filedialog.askopenfilename(title="Selecciona un archivo")
    
#     if ruta_archivo:
#         # Mostrar la ruta seleccionada en la etiqueta
#         etiqueta.config(text=f"Archivo seleccionado: {ruta_archivo}")
#     else:
#         etiqueta.config(text="No se seleccionó ningún archivo")

# def encriptar_archivo():
#     # Abirmos el archivo
#     archivo = open(ruta_archivo, 'rb')
#     print(archivo.read())
#     archivo.close()

# # Crear la ventana principal
# ventana = tk.Tk()
# ventana.title("Protector de archivos 3000")

# # Crear un botón que llame a la función para seleccionar el archivo
# boton = tk.Button(ventana, text="Seleccionar archivo", command=seleccionar_archivo)
# boton.pack(pady=10)

# # Crear un botón que llame a la función para encriptar el archivo
# boton = tk.Button(ventana, text="Encriptar archivo", command=encriptar_archivo)
# boton.pack(pady=10)

# # Crear una etiqueta para mostrar la ruta del archivo seleccionado
# etiqueta = tk.Label(ventana, text="No se ha seleccionado ningún archivo.")
# etiqueta.pack(pady=10)

# # Ejecutar la ventana principal
# ventana.mainloop()

import tkinter as tk
from tkinter import filedialog
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

# Variables globales
ruta_archivo = None
key = get_random_bytes(16)  # Clave AES-128 generada aleatoriamente

# Función que se ejecuta cuando se presiona el botón para seleccionar archivo
def seleccionar_archivo():
    global ruta_archivo
    ruta_archivo = filedialog.askopenfilename(title="Selecciona un archivo")
    
    if ruta_archivo:
        etiqueta.config(text=f"Archivo seleccionado: {ruta_archivo}")
    else:
        etiqueta.config(text="No se seleccionó ningún archivo")

# Función para encriptar el archivo seleccionado
def encriptar_archivo():
    if ruta_archivo:
        try:
            # Leer el archivo en modo binario
            with open(ruta_archivo, 'rb') as archivo:
                datos = archivo.read()

            # Crear un objeto de cifrado AES en modo EAX
            cipher = AES.new(key, AES.MODE_EAX)
            ciphertext, tag = cipher.encrypt_and_digest(datos)

            # Guardar el archivo encriptado
            ruta_encriptada = ruta_archivo + '.enc'
            with open(ruta_encriptada, 'wb') as archivo_encriptado:
                archivo_encriptado.write(cipher.nonce)  # Escribir el nonce
                archivo_encriptado.write(tag)           # Escribir el tag
                archivo_encriptado.write(ciphertext)    # Escribir el texto cifrado

            etiqueta.config(text=f"Archivo encriptado guardado en: {ruta_encriptada}")
        except Exception as e:
            etiqueta.config(text=f"Error al encriptar el archivo: {str(e)}")
    else:
        etiqueta.config(text="Primero selecciona un archivo para encriptar.")

# Configuración de la interfaz gráfica
ventana = tk.Tk()
ventana.title("Encriptar Archivo AES")
ventana.geometry("400x300")

# Botón para seleccionar el archivo
boton_seleccionar = tk.Button(ventana, text="Seleccionar archivo", command=seleccionar_archivo)
boton_seleccionar.pack(pady=20)

# Botón para encriptar el archivo seleccionado
boton_encriptar = tk.Button(ventana, text="Encriptar archivo", command=encriptar_archivo)
boton_encriptar.pack(pady=20)

# Etiqueta para mostrar mensajes al usuario
etiqueta = tk.Label(ventana, text="No se ha seleccionado ningún archivo.")
etiqueta.pack(pady=20)

# Ejecutar la ventana
ventana.mainloop()
