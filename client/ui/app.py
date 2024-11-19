import customtkinter
from ui.home import Home

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x480")
        self.title("Asegurados")
        self._set_appearance_mode("light")
        self.configure(bg = "white")
        self.frames = {}
        container = customtkinter.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        for F in (Home, Home):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(Home)
            
    def show_frame(self, context):
        frame = self.frames[context]
        frame.tkraise()