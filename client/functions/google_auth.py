import json
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import requests
from functions.google_user import GoogleUser

flow = InstalledAppFlow.from_client_secrets_file(
    'secrets.json',
    scopes=['https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile', 'openid'])

# Abre un navegador para que el usuario elija la cuenta de google con la que autenticarse
# y devuelve un objeto GoogleUser con la info del usuario autenticado
# Se puede usar para obtener el email y nombre del usuario al registrarlo
def get_google_user() -> GoogleUser:
    flow.run_local_server()
    credentials = flow.credentials

    user_info_service = build('oauth2', 'v2', credentials=credentials)
    user_info = user_info_service.userinfo().get().execute()

    return GoogleUser.from_dict(user_info)

# Abre un navegador para que el usuario elija la cuenta de google con la que autenticarse,
# llama al servicio de login de google y devuelve el resultado (userId y privateRSA)
def google_login():
    flow.run_local_server()
    id_token = flow.credentials.id_token
    
    loginGoogle = requests.post('http://localhost:5000/users/login-google', json={"idToken": id_token})
    return json.loads(loginGoogle.text)
