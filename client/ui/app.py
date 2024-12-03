import customtkinter
from customtkinter import set_appearance_mode
from ui.home import Home
from ui.otp_qr_code import OtpQrCode
from ui.login import Login
from ui.register import Register 
from ui.subir_archivo import SubirArchivo
from CTkMessagebox import CTkMessagebox
from ui.shareFile import Share
from ui.SharedFileInfo import SharedInfo
from functions import debug
from functions.consts import server

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        self.geometry("600x480")
        self.title("Asegurados")
        set_appearance_mode("light")
        self.configure(bg = "white")
        self.frames = {}
        self.user = None
        self.server = server

        self.container = customtkinter.CTkFrame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        for F in (Login, Register):
            frame = self.generate_frame(F)
            self.frames[F] = frame
        
        self.show_frame("Login")
            
    def show_frame(self, contextParam, params = None):
        
        if ( contextParam is None or contextParam == "" ):
            print(debug.printMoment(), "No context param!...")
            return
        
        translated_context = {
            "Login": Login,
            "Register": Register,
            "Home": Home,
            "SubirArchivo": SubirArchivo,
            "Compartir": Share,
            "InfoComportido": SharedInfo,
            "OtpQrCode": OtpQrCode
        }
        
        print(debug.printMoment(), f"Mostrando... [{contextParam}]" )
        
        context = translated_context[contextParam]
        
        needs_reload = [ translated_context["Home"], translated_context["Compartir"], translated_context["InfoComportido"] ]
        needs_params = [ translated_context["Compartir"], translated_context["InfoComportido"] ]
        
        frame = self.frames[context]
                
        frame.tkraise()
        
        if ( context in needs_reload ):
            if ( context in needs_params ):
                print(debug.printMoment(), f"Reloading with params... [{contextParam}]")
                self.frames[context].reload(params)
            else:
                print(debug.printMoment(), f"Reloading... [{contextParam}]")
                self.frames[context].reload()
    
    def generate_frame(self, F):
        frame = F(self.container, self)
        frame.grid(row=0, column=0, sticky="nsew")
        return frame
        
    def load_restricted_frames(self):
        for F in (Home, SubirArchivo, Share, SharedInfo, OtpQrCode):
            frame = self.generate_frame(F)
            self.frames[F] = frame
            self.show_frame("Login")
        print(debug.printMoment(), "generated restricted frames... ", self.frames)
            
    def show_error(self, message):
        CTkMessagebox(title="Error", message=message, icon="cancel")
    
    def show_success(self, message):
        CTkMessagebox(title="Error", message=message, icon="check")