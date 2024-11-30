from customtkinter import CTkFrame, CTkLabel, CTkButton
from functions.file_requests import download_file
from functions.encrypt_decrypt import decrypt
import functions.file_requests as file_request
import requests

class Home(CTkFrame):
    def __init__(self, parent, controller):
        CTkFrame.__init__(self, parent)
        self.controller = controller
        self.firstTime = True
        
        self.archivos = self.getFiles()
        self.archivosCompartidos = self.getSharedFiles()
        self.archivosCompartidosConmigo = self.getSharedWithMeFiles()
        
        self.showing = 0
        
        header_frame = CTkFrame(self, fg_color="transparent")
        header_frame.pack(pady=(30, 20), padx=20, fill="x")
        
        title = CTkLabel(master=header_frame, text="Página principal", font=("Arial", 24, "bold"), 
            text_color="#601E88", anchor="w", justify="left")
        title.pack(side="left")
        
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
      
        self.btn_compartidos_por_mi.pack(padx=(5, 5), side = "right")
        
        self.table = CTkFrame(master=self, bg_color="transparent", fg_color="transparent")
        self.generateTable()
        self.table.pack()

    def getFiles(self):
        response = ""
        try:
            response = requests.get(f'http://localhost:5000/files/{self.controller.user.userId}')
            response.raise_for_status()
            archivos = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener archivos: {e}")
        finally: 
            return archivos
        
    def getSharedFiles(self):
        response = ""
        try:
            response = requests.get(f'http://localhost:5000/shared-files-of/{self.controller.user.userId}')
            response.raise_for_status()
            archivos = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener archivos: {e}")
        finally: 
            return archivos
        
    def getSharedWithMeFiles(self):
        response = ""
        try:
            response = requests.get(f'http://localhost:5000/shared-files-to/{self.controller.user.userId}')
            response.raise_for_status()
            archivos = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener archivos: {e}")
        finally: 
            return archivos

    def generateTable(self):
        print("Generating...")
        match self.showing:
            case 0:
                files = self.archivos
                print("my files")
            case 1:
                files = self.archivosCompartidos
                print("my shared files")
            case 2:
                files = self.archivosCompartidosConmigo
                print("shared with me files")
         
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
                        fg_color="#9674AC",
                        hover_color="#EC5E5E",
                        text_color="#FFFFFF",
                        width = 5,
                        command=lambda archivo_id=row[0]: self.eliminar_archivo(archivo_id=archivo_id)  # Pasa el ID del archivo al botón
                    )
                    
                    btn_action.pack(side="right", padx=(2, 0))
                    
                if ( self.showing == 0 or self.showing == 1 ): 
                    btn_action = CTkButton(
                        master=row_frame,
                        text="Compartir",
                        corner_radius=32,
                        fg_color="#601E88",
                        hover_color="#EC5E5E",
                        text_color="#FFFFFF",
                        width = 5,
                        command=lambda archivo_id=row[0]: self.compartir_archivo(archivo_id=archivo_id)  # Pasa el ID del archivo al botón
                    )
                    
                    btn_action.pack(side="right", padx=(2, 0))
                    
                if ( self.showing == 1 ): 
                    btn_action = CTkButton(
                        master=row_frame,
                        text="No compartir",
                        corner_radius=32,
                        fg_color="#601E88",
                        hover_color="#EC5E5E",
                        text_color="#FFFFFF",
                        width = 5,
                        command=lambda archivo_id=row[0]: self.compartir_archivo(archivo_id=archivo_id)  # Pasa el ID del archivo al botón
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
        print("reloading...")
        if ( self.firstTime ):
            print("first time")
            self.firstTime = False
            return
        
        self.table.destroy()
        self.table = CTkFrame(master=self, bg_color="transparent", fg_color="transparent")
        
        match self.showing:
            case 0:
                print("showing 0")
                self.archivos = self.getFiles()
                
            case 1:
                print("showing 1")
                self.archivosCompartidos = self.getSharedFiles()
                
            case 2:
                print("showing 2")
                self.archivosCompartidosConmigo = self.getSharedWithMeFiles()
                
        self.generateTable()
        self.table.pack()

    def swap_table(self, table):
        self.showing = table
        
        match self.showing:
            case 0:
                print("swapping to table 0")
                self.btn_mis_archivos.configure(state="disabled")
                self.btn_compartidos_por_mi.configure(state="normal")
                self.btn_compartidos_conmigo.configure(state="normal")
            case 1:
                print("swapping to table 1")
                self.btn_mis_archivos.configure(state="normal")
                self.btn_compartidos_por_mi.configure(state="disabled")
                self.btn_compartidos_conmigo.configure(state="normal")
            case 2:
                print("swapping to table 2")
                self.btn_mis_archivos.configure(state="normal")
                self.btn_compartidos_por_mi.configure(state="normal")
                self.btn_compartidos_conmigo.configure(state="disabled")
                
        self.reload()

    def procesar_guardado(self, archivo_id, nombre_archivo):
        nombre_archivo = str(nombre_archivo)
        download_file(archivo_id, nombre_archivo)
        fileInfo = file_request.get_file_info(archivo_id)    
        # (user: User, file_name, encrypted_file, file_aes_key_encrypted, file_type, signatory_public_key, signature):
                # decrypt(self.controller.user, nombre_archivo, str(fileInfo["body"]["fileName"]), str(fileInfo["body"]["fileName"]) + fileInfo["body"]["fileType"], fileInfo["body"]["aesKey"], fileInfo["body"]["fileType"], fileInfo["body"]["signature"])

                # decrypt(user = self.controller.user, 
                #         file_name = nombre_archivo,
                #         encrypted_file = str(fileInfo["body"]["encryptedFile"]), 
                #         file_aes_key_encrypted = fileInfo["body"]["aesKey"], 
                #         file_type = fileInfo["body"]["fileType"], 
                #         signatory_public_key = fileInfo["body"]["signature"], 
                #         signature = fileInfo["body"]["signature"])

        decrypt(user = self.controller.user, 
            file_name = nombre_archivo,
            encrypted_file = nombre_archivo, 
            file_aes_key_encrypted = fileInfo["body"]["aesKey"], 
            file_type = fileInfo["body"]["fileType"], 
            signatory_public_key = fileInfo["body"]["signature"], 
            signature = fileInfo["body"]["signature"])

    def eliminar_archivo(archivo_id):
        response = requests.delete(f'http://localhost:5000/files', json={"fileId": archivo_id})
        response.raise_for_status()
        response = response.json()

    def compartir_archivo(self, archivo_id):
        self.controller.show_frame("Compartir")
        
    def on_subir_archivo(self):
        self.controller.show_frame("SubirArchivo")