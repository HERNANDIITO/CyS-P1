from customtkinter import CTkFrame, CTkLabel, CTkButton

# Fichero preparador para copiar y pegar.
# Asi sera mas facil añadir pantallas nuevas
# Que no se os olvide añadir la clase en app.py > show_frame() > translated_context
# como clave pon un string representativo y como contenidos pon la clase del objeto, por ejemplo:

# translated_context = {
#     "Login": Login,
#     "Register": Register,
#     "Home": Home,
#     "SubirArchivo": SubirArchivo,
#     "Template": Template
# }

class Template(CTkFrame):
    def __init__(self, parent, controller):
        # NO BORRAR
        CTkFrame.__init__(self, parent)
        self.controller = controller
        # no te olvides de agregar la clase en app.py funcion show_frame objeto translated_context para poder nevegar a ella
        # NO BORRAR
        
        # Borrar a partir de aqui
        
        title = CTkLabel(master=self, text="Template working!", font=("Arial", 24, "bold"), 
            text_color="#601E88", anchor="w", justify="left")
        title.pack(side="left")
        
        btn_nav = CTkButton(
            master = self,
            text = "Ir a subir archivo",
            corner_radius = 32,
            fg_color = "#601E88",
            hover_color = "#D18AF0",
            text_color = "#ffffff",
            command = self.cambiarVentana
        )
        
        btn1 = CTkButton(
            master = self,
            text = "Ir a subir archivo",
            corner_radius = 32,
            fg_color = "#601E88",
            hover_color = "#D18AF0",
            text_color = "#ffffff",
            command = self.func1
        )


    def func1(self):  # Borrable
        print("func1!")

    def cambiarVentana(self): # Borrable
        # Ver: app.py funcion show_frame objeto translated_context
        self.controller.show_frame("nombreVentana")