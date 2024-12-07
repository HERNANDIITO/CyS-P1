from customtkinter import *
from functions.result import Result
from tkinter import filedialog
from functions.encrypt_decrypt import encrypt

class SubirArchivo(CTkFrame):
    def __init__(self, parent, controller):
        CTkFrame.__init__(self, parent)
        self.controller = controller
        self.archivo_path = None
        self.archivo_cifrado_label = ""
        self.archivo_subido_label = ""

        # Título grande centrado en morado
        title_label = CTkLabel(master=self, text="Protege tus archivos", 
                            text_color="#601E88", font=("Arial Bold", 24, "bold"))
        title_label.pack(pady=(40, 5)) 

        # Subtítulo centrado en gris
        subtitle_label = CTkLabel(master=self, text="Sube tus archivos y cífralos aquí", 
                                text_color="#606060", font=("Arial", 15))
        subtitle_label.pack(pady=(5, 40))

        # Botón para "Seleccionar archivo"
        seleccionar_button = CTkButton(master=self, text="Seleccionar archivo", 
                                    fg_color="#601E88", text_color="white", font=("Arial", 14),
                                    hover_color="#D18AF0", corner_radius=32, width=200,
                                    command=self.seleccionar_archivo)
        seleccionar_button.pack(pady=(5, 20)) 

        # Etiqueta para mostrar el estado del archivo subido (vacía por defecto)
        self.archivo_subido_label = CTkLabel(master=self, text="", 
                                        text_color="green", font=("Arial", 12))


        # Botón para cifrar archivo
        cifrar_button = CTkButton(master=self, text="Cifrar archivo", 
                                fg_color="#601E88", text_color="white", font=("Arial", 14),
                                hover_color="#D18AF0", corner_radius=32,  width=200,
                                command=self.on_cifrar_archivo)
        cifrar_button.pack(pady=(5, 20))

        # Etiqueta para mostrar si el archivo se ha cifrado bien (vacía por defecto)
        
        self.archivo_cifrado_label = CTkLabel(master=self, text="", 
                                        text_color="green", font=("Arial", 12))

        # Botón volver
        volver_button = CTkButton(master=self, text="Volver", fg_color="#601E88", 
                                text_color="white", font=("Arial", 12), 
                                hover_color="#D18AF0", corner_radius=32, width=20,
                                command=self.on_volver)
        volver_button.place(x=20, y=20)  # Colocar en la parte inferior izquierda

    def on_volver(self):
        self.controller.show_frame("Home")
        
    def seleccionar_archivo(self):
        self.archivo_path = None

        # Abrir explorador de archivos
        archivo = filedialog.askopenfilename(title="Seleccionar archivo")
        
        if archivo:
            self.archivo_path = archivo
            # Mostrar texto debajo del botón si el archivo se selecciona
            self.archivo_subido_label.configure(text=f"Archivo seleccionado correctamente: {archivo.split('/')[-1]}", text_color="green")
            self.archivo_subido_label.pack(pady=(5, 20))

            self.archivo_cifrado_label.configure(text="", text_color="orange")
            self.archivo_cifrado_label.pack(pady=(5, 20))
        else:
            self.archivo_path = None
            self.archivo_subido_label.configure(text="No se ha seleccionado ningún archivo", text_color="red")
            self.archivo_subido_label.pack(pady=(5, 20))

    def on_cifrar_archivo(self): 
        if self.archivo_path is None:
            self.controller.show_error("Debe subir un archivo para encriptar")
            self.archivo_cifrado_label.configure(text="Seleccione un archivo antes de cifrar", text_color="orange")
            self.archivo_cifrado_label.pack(pady=(5, 20))
            return

        response = encrypt(self.archivo_path, self.controller.user)
        
        if ( type(response) is Result ):
            self.controller.show_error(response.msg)
            return
            
        
        self.archivo_path = None   #reinicia el archivo seleccionado a vacio
        self.archivo_cifrado_label.configure(text="Archivo cifrado correctamente", text_color="blue")
        self.archivo_cifrado_label.pack(pady=(5, 20))

        self.archivo_subido_label.configure(text="", text_color="red")
        self.archivo_subido_label.pack(pady=(5, 20))