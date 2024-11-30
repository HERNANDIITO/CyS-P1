import customtkinter
from customtkinter import set_appearance_mode
from ui.home import Home
from ui.login import Login
from ui.register import Register 
from ui.subir_archivo import SubirArchivo
from CTkMessagebox import CTkMessagebox
from ui.shareFile import Share
from ui.SharedFileInfo import SharedInfo



class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        self.geometry("600x480")
        self.title("Asegurados")
        set_appearance_mode("light")
        self.configure(bg = "white")
        self.frames = {}
        self.user = None
        self.server = "http://127.0.0.1:5000"
        
        self.container = customtkinter.CTkFrame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        for F in (Login, Register):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame("Login")
            
    def show_frame(self, contextParam, params = None):
        
        translated_context = {
            "Login": Login,
            "Register": Register,
            "Home": Home,
            "SubirArchivo": SubirArchivo,
            "Compartir": Share,
            "InfoComportido": SharedInfo
        }
        
        context = translated_context[contextParam]
        
        needs_reload = [ translated_context["Home"], translated_context["Compartir"] ]
        needs_params = [ translated_context["Compartir"] ]
        
        frame = self.frames[context]
                
        frame.tkraise()
        
        if ( context in needs_reload ):
            if ( context in needs_params ):
                self.frames[context].reload(params)
            else:
                self.frames[context].reload()
        
    def load_restricted_frames(self):
        for F in (Home, SubirArchivo, Share, SharedInfo):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
    def show_error(self, message):
        CTkMessagebox(title="Error", message=message, icon="cancel")