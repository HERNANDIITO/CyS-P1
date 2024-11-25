import customtkinter
from customtkinter import set_appearance_mode
from ui.home import Home
from ui.login import Login
from ui.register import Register 
from ui.subir_archivo import SubirArchivo
from CTkMessagebox import CTkMessagebox

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
            
    def show_frame(self, context):
        
        translated_context = {
            "Login": Login,
            "Register": Register,
            "Home": Home,
            "SubirArchivo": SubirArchivo
        }
        
        frame = self.frames[translated_context[context]]
        frame.tkraise()
        
    def load_restricted_frames(self):
        for F in (Home, SubirArchivo):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
    def show_error(self, message):
        CTkMessagebox(title="Error", message=message, icon="cancel")