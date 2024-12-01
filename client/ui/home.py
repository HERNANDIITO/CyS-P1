from customtkinter import CTkFrame, CTkLabel, CTkButton
from functions.file_requests import download_file
from functions.encrypt_decrypt import decrypt
import functions.file_requests as file_request
from functions import debug
import requests, threading

class Home(CTkFrame):
    def __init__(self, parent, controller):
        print(debug.printMoment(), "Home init...")
        CTkFrame.__init__(self, parent)
        self.controller = controller
        self.firstTime = True
        
        self.archivos = None
        self.archivosCompartidos = None
        self.archivosCompartidosConmigo = None
        
        self.showing = 0
        
        header_frame = CTkFrame(self, fg_color="transparent")
        header_frame.pack(pady=(30, 20), padx=20, fill="x")
        
        title = CTkLabel(master=header_frame, text="Página principal", font=("Arial", 24, "bold"), 
            text_color="#601E88", anchor="w", justify="left")
        title.pack(side="left")
        
        print(debug.printMoment(), "btn_selec_archivo...")
        
        btn_selec_archivo = CTkButton(
            master = header_frame,
            text = "Subir archivo",
            corner_radius = 32,
            fg_color = "#601E88",
            hover_color = "#D18AF0",
            text_color = "#ffffff",
            command = self.on_subir_archivo
        )
      
        btn_selec_archivo.pack(side="right")
        
        archivosCompartidos = CTkFrame(master=self, bg_color="transparent", fg_color="transparent")
        archivosCompartidos.pack()
        print(debug.printMoment(), "archivosCompartidos...")
        
        self.btn_mis_archivos = CTkButton(
            master = archivosCompartidos,
            text = "Mis archivos",
            corner_radius = 32,
            fg_color = "#601E88",
            hover_color = "#D18AF0",
            text_color = "#ffffff",
            state="disabled",
            command = lambda pageToShow = 0 : self.swap_table(table=pageToShow)
        )
        
        self.btn_mis_archivos.pack(side="left")
        
        self.btn_compartidos_conmigo = CTkButton(
            master = archivosCompartidos,
            text = "Compartidos conmigo",
            corner_radius = 32,
            fg_color = "#601E88",
            hover_color = "#D18AF0",
            text_color = "#ffffff",
            command = lambda pageToShow = 2 : self.swap_table(table=pageToShow)
        )
      
        self.btn_compartidos_conmigo.pack(side="right")
        
        self.btn_compartidos_por_mi = CTkButton(
            master = archivosCompartidos,
            text = "Compartidos por mí",
            corner_radius = 32,
            fg_color = "#601E88",
            hover_color = "#D18AF0",
            text_color = "#ffffff",
            command = lambda pageToShow = 1 : self.swap_table(table=pageToShow)
        )
        
        print(debug.printMoment(), "buttons...")
      
        self.btn_compartidos_por_mi.pack(padx=(5, 5), side = "right")
        
        self.table = CTkFrame(master=self, bg_color="transparent", fg_color="transparent")
        
        print(debug.printMoment(), "table generated...")

        # borrar abajo
        self.info_button_frame = CTkFrame(master=self, bg_color="transparent", fg_color="transparent")
        self.info_button_frame.pack(pady=10)  # Añade algo de margen entre la tabla y el botón

        self.info_button = CTkButton(
            master=self.info_button_frame,
            text="Info Archivo Compartido",
            corner_radius=32,
            fg_color="#601E88",
            hover_color="#D18AF0",
            text_color="#ffffff",
            command=lambda: self.info_archivo_compartido(archivo_id=0)
        )
        self.info_button.pack(pady=5)  # Añade margen alrededor del botón
        # borrar arriba

    def getFiles(self):
        print(debug.printMoment(), "getFiles...")
        response = ""
        try:
            print(debug.printMoment(), "sending request...")
            response = requests.get(f'{self.controller.server}/files/{self.controller.user.userId}')
            print(debug.printMoment(), "got response...")
            response.raise_for_status()
            print(debug.printMoment(), "archivos to json...")
            archivos = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener archivos: {e}")
        finally: 
            print(debug.printMoment(), "getFiles ended...")
            return archivos
        
    def getSharedFiles(self):
        print(debug.printMoment(), "getSharedFiles...")
        response = ""
        try:
            response = requests.get(f'{self.controller.server}/shared-files-of/{self.controller.user.userId}')
            response.raise_for_status()
            archivos = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener archivos: {e}")
        finally: 
            print(debug.printMoment(), "getSharedFiles ended...")
            return archivos
        
    def getSharedWithMeFiles(self):
        print(debug.printMoment(), "getSharedWithMeFiles...")
        response = ""
        try:
            response = requests.get(f'{self.controller.server}/shared-files-to/{self.controller.user.userId}')
            response.raise_for_status()
            archivos = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener archivos: {e}")
        finally: 
            print(debug.printMoment(), "getSharedWithMeFiles ended...")
            return archivos

    def generateTable(self):
        print(debug.printMoment(), "Generating...")
        match self.showing:
            case 0:
                files = self.archivos
                print(debug.printMoment(), "my files")
            case 1:
                files = self.archivosCompartidos
                print(debug.printMoment(), "my shared files")
            case 2:
                files = self.archivosCompartidosConmigo
                print(debug.printMoment(), "shared with me files")
         
        # Inicializar la tabla de datos con encabezados
        table_data = [
            ["ID", "Nombre de archivo"]
        ]
        
        # Comprueba que el usuario tenga al menos un fichero
        if (files["body"]):
            # Rellenar la tabla con los datos obtenidos de la respuesta del servidor
            for archivo in files["body"]["files"]:
                archivo_id = archivo["fileId"]
                nombre_archivo = str(archivo["fileName"]) + archivo["fileType"]
                table_data.append([archivo_id, nombre_archivo])

        # Crear las filas manualmente con botones a la derecha
        for idx, row in enumerate(table_data):
            # Establecer el marco de la fila
            if idx == 0:
                row_frame = CTkFrame(master=self.table, fg_color="#601E88", border_color="#601E88", corner_radius=32, border_width=2)
                row_frame.pack(fill="x", padx=20, pady=5)
            else:
                row_frame = CTkFrame(master=self.table, fg_color="#FFFFFF", corner_radius=32)
                row_frame.pack(fill="x", padx=20, pady=5)

            # Añadir celdas a la fila
            for cell in row:
                text_color = "#FFFFFF" if idx == 0 else "#000000"
                cell_label = CTkLabel(master=row_frame, text=cell, text_color=text_color, corner_radius=32, anchor="w")
                cell_label.pack(side="left", padx=10)

            # Añadir el botón de descarga a la derecha si no es la fila de encabezado
            if idx != 0:
                if ( self.showing == 0 ): 
                    btn_action = CTkButton(
                        master=row_frame,
                        text="Eliminar",
                        corner_radius=32,
                        fg_color="#881e1e",
                        hover_color="#b85c5c",
                        text_color="#FFFFFF",
                        width = 5,
                        command=lambda archivo_id=row[0]: self.eliminar_archivo(archivo_id=archivo_id)  # Pasa el ID del archivo al botón
                    )
                    
                    btn_action.pack(side="right", padx=(2, 0))
                    
                if ( self.showing == 0 ): 
                    btn_action = CTkButton(
                        master=row_frame,
                        text="Compartir",
                        corner_radius=32,
                        fg_color="#601E88",
                        hover_color="#D18AF0",
                        text_color="#FFFFFF",
                        width = 5,
                        command=lambda archivo_id=row[0]: self.compartir_archivo(archivo_id=archivo_id)  # Pasa el ID del archivo al botón
                    )
                    
                    btn_action.pack(side="right", padx=(2, 0))
                    
                if ( self.showing == 1 ): 

                    btn_action = CTkButton(
                        master=row_frame,
                        text="eliminar comparticion",
                        corner_radius=32,
                        fg_color="#881e1e",
                        hover_color="#EC5E5E",
                        text_color="#FFFFFF",
                        width = 5,
                        command=lambda archivo_id=row[0]: self.eliminar_comparticion(archivo_id=archivo_id)  # Pasa el ID del archivo al botón
                    )
                    
                    btn_action.pack(side="right", padx=(2, 0))

                    btn_action = CTkButton(
                        master=row_frame,
                        text="info de comparticion",
                        corner_radius=32,
                        fg_color="#601E88",
                        hover_color="#D18AF0",
                        text_color="#FFFFFF",
                        width = 5,
                        command=lambda archivo_id=row[0]: self.info_archivo_compartido(archivo_id=archivo_id)  # Pasa el ID del archivo al botón
                    )   
                    btn_action.pack(side="right", padx=(2, 0))




                btn_action = CTkButton(
                    master=row_frame,
                    text="Descargar",
                    corner_radius=32,
                    fg_color="#601E88",
                    hover_color="#D18AF0",
                    text_color="#ffffff",
                    width = 5,
                    command=lambda archivo_id=row[0], nombre_archivo=row[1]: self.procesar_guardado(archivo_id, nombre_archivo)  # Pasa el ID del archivo al botón
                )
                btn_action.pack(side="right", padx=(2, 0))

    def reload(self):
        print(debug.printMoment(), "reloading home...")
        
        self.table.destroy()
        self.table = CTkFrame(master=self, bg_color="transparent", fg_color="transparent")
        
        match self.showing:
            case 0:
                print(debug.printMoment(), "showing 0")
                self.archivos = self.getFiles()
                
            case 1:
                print(debug.printMoment(), "showing 1")
                self.archivosCompartidos = self.getSharedFiles()
                
            case 2:
                print(debug.printMoment(), "showing 2")
                self.archivosCompartidosConmigo = self.getSharedWithMeFiles()
                
        self.generateTable()
        self.table.pack()

    def swap_table(self, table):
        self.showing = table
        
        match self.showing:
            case 0:
                print(debug.printMoment(), "swapping to table 0")
                self.btn_mis_archivos.configure(state="disabled")
                self.btn_compartidos_por_mi.configure(state="normal")
                self.btn_compartidos_conmigo.configure(state="normal")
            case 1:
                print(debug.printMoment(), "swapping to table 1")
                self.btn_mis_archivos.configure(state="normal")
                self.btn_compartidos_por_mi.configure(state="disabled")
                self.btn_compartidos_conmigo.configure(state="normal")
            case 2:
                print(debug.printMoment(), "swapping to table 2")
                self.btn_mis_archivos.configure(state="normal")
                self.btn_compartidos_por_mi.configure(state="normal")
                self.btn_compartidos_conmigo.configure(state="disabled")
                
        hilo = threading.Thread(target=self.reload)
        hilo.daemon = True  # Asegura que el hilo se cierre al cerrar la app
        hilo.start()

    def procesar_guardado(self, archivo_id, nombre_archivo):
        
        nombre_archivo = str(nombre_archivo)
        download_file(archivo_id, nombre_archivo)
        fileInfo = file_request.get_file_info(archivo_id)    
        
        decrypt(user = self.controller.user, 
            file_name = nombre_archivo,
            encrypted_file = nombre_archivo, 
            file_aes_key_encrypted = fileInfo["body"]["aesKey"], 
            file_type = fileInfo["body"]["fileType"], 
            signatory_public_key = fileInfo["body"]["signature"], 
            signature = fileInfo["body"]["signature"])

    def eliminar_archivo(self, archivo_id):
        response = requests.delete(f'{self.controller.server}/files', json={"fileId": archivo_id})
        response.raise_for_status()
        response = response.json()

    def compartir_archivo(self, archivo_id):
        self.controller.show_frame("Compartir", archivo_id)

    def info_archivo_compartido(self, archivo_id):
        self.controller.show_frame("InfoComportido", archivo_id)

    def eliminar_comparticion(self, archivo_id):
        print("logica de eliminar comparticion no implementada")
        
    def on_subir_archivo(self):
        self.controller.show_frame("SubirArchivo")