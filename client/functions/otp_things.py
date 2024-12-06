import json
import requests
from functions.consts import server

# Obtiene la URL que se usa para generar el codigo QR
def obtain_user_url(user_id) -> str:
    r = requests.get(f'{server}/otp-url/{user_id}')
    mapRes = json.loads(r.text)
    return mapRes["body"]["url"]

# Comprueba si el codigo OTP es correcto
def check_otp(user_id, otp_code):
    r = requests.post(f'{server}/users/check-otp', json={"user_id": user_id, "otp_code": otp_code})
    mapRes = json.loads(r.text)
    return mapRes
