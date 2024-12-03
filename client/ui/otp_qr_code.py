from customtkinter import CTkFrame, CTkLabel, CTkButton
from ui.components import image_qr
from functions.otp_things import obtain_user_url

class OtpQrCode(CTkFrame):
    def __init__(self, parent, controller):
        CTkFrame.__init__(self, parent)
        self.controller = controller
        
        url = obtain_user_url(self.controller.user.userId)
        
        CTkLabel(master=self, text='Escanea este código para guardar el doble factor de autenticación.').pack()
        CTkLabel(master=self, text='¡CUIDADO! Una vez cerrado, no podrás recuperar este código QR.').pack()
        image_qr.ImageQr(self, url)
        CTkButton(master=self, text="Continuar", command=self.cambiarVentana).pack()

    def cambiarVentana(self):
        self.controller.show_frame("Home")
