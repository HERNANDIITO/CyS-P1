# Nota: El archivo secrets.json NO deberia subirse al repositorio, ya que contiene credenciales privadas de la API de Google
# En este caso lo he subido ya que el repositorio es privado y tampoco pasaria nada si me robasen esas credenciales

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Configura el flujo de autenticacion para que use el archivo secrets.json (contiene las credenciales de la API de Google) en la carpeta actual
# y especifica los permisos que se solicitaran al usuario (email, info del perfil y el openid que aun no se muy bien que hace)
flow = InstalledAppFlow.from_client_secrets_file(
    'secrets.json',
    scopes=['https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile', 'openid'])

# Abre un navegador para que el usuario elija la cuenta de google con la que iniciar sesion
flow.run_local_server()
credentials = flow.credentials

# Obtiene la info del usuario
user_info_service = build('oauth2', 'v2', credentials=credentials)
user_info = user_info_service.userinfo().get().execute()

# Imprime el email del usuario. Tambien se puede obtener el id, nombre, foto de perfil y otros datos
print("Email usuario autenticado: " + user_info['email'])