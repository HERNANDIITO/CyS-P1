from customtkinter import CTkFrame, CTkLabel, CTkButton, CTkInputDialog
from ui.components import image_qr
from functions.otp_things import obtain_user_url
import queue, threading
from functions import user_auth, debug
from functions.user import User

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
        dialog = CTkInputDialog(text="Escribe tu código de doble factor de autenticación:", title="Código OTP")
        otp_code = dialog.get_input()

        result_queue = queue.Queue()
        hilo = threading.Thread(target=user_auth.check2fa, args=(self.controller.user, otp_code, result_queue))
        hilo.daemon = True  # Asegura que el hilo se cierre al cerrar la app
        hilo.start()
        hilo.join()
        result = result_queue.get()
        
        if ( type(result) is User ):
            print(debug.printMoment(), "usuario registrado: ", self.controller.user)
            self.controller.load_restricted_frames()
            print(debug.printMoment(), "mostrando home...")
            self.controller.show_frame("Home")
        else:
            self.controller.show_error("Código OTP incorrecto")

