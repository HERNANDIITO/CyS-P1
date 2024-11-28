from customtkinter import *
import qrcode

# Componente para mostrar un codigo QR con el texto especificado en una interfaz
# Uso: image_qr.ImageQr(frame, 'https://www.youtube.com/watch?v=xvFZjo5PgG0')
class ImageQr:
    def __init__(self, master, qr_code_text: str):
        self._qr_code_text = qr_code_text
        self._qr_label = CTkLabel(master, text="")
        self.generate_qr()
        
    def generate_qr(self):
        # Genera el codigo QR
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(self._qr_code_text)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
        # Carga la imagen del codigo QR
        qr_img_tk = CTkImage(light_image=qr_img.get_image(), dark_image=qr_img.get_image(), size=(200, 200))
        
        # Actualiza el label con el codigo QR
        self._qr_label.configure(image=qr_img_tk)
        self._qr_label.image = qr_img_tk
        self._qr_label.pack(expand=True)
