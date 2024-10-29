import json
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import requests
from functions.aes import decrypt_private_key_with_aes
from functions.rsa import import_private_key, import_public_key
from functions.user import User
from functions.google_user import GoogleUser
import os

flow = InstalledAppFlow.from_client_secrets_file(
    os.path.join(os.path.dirname(__file__), Path('secrets.json')),
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
def google_login() -> User | None:
    flow.run_local_server()
    id_token = flow.credentials.id_token
    
    loginGoogle = requests.post('http://localhost:5000/users/login-google', json={"idToken": id_token})
    
    # A partir de aqui es el mismo proceso que un login normal
    # TODO: Necesito la pass del usuario, tengo que pensar en como arreglarlo
    
    login_result_json = json.loads(loginGoogle.text)
    
    if(str(json.loads(loginGoogle.text)["code"]) == "200"):
        
        # hacer una peticion que me devuelva la clave privada del usuario
        userID      = login_result_json["body"]["userID"]
        privateRSA  = login_result_json["body"]["privateRSA"]
        publicRSA   = login_result_json["body"]["publicRSA"]
        
        # desencriptar con aes la pass_hash_part2, descifrar y guardar en local
        
        # Las claves no van y no puedo mas :C
        importedPublicKey  = import_public_key(public_key_pem = publicRSA)
        
        #decryptedPrivateKey = decrypt_private_key_with_aes(encrypted_private_key_pem=privateRSA, aes_key='Esto no vaEsto no vaEsto no vaEsto no vaEsto no vaEsto no vaEsto no vaEsto no vaEsto no vaEsto no vaEsto no vaEsto no vaEsto nov')
        
        #importedPrivateKey = import_private_key(private_key_pem = 'esto no va')
            
        user = User( userId= userID, privateRSA= 'esto no va', publicRSA= importedPublicKey )
        
        return user
    
    return None
    #return json.loads(loginGoogle.text)
