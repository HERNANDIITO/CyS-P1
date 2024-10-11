from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from google_user import GoogleUser

flow = InstalledAppFlow.from_client_secrets_file(
    'secrets.json',
    scopes=['https://www.googleapis.com/auth/userinfo.email', 'https://www.googleapis.com/auth/userinfo.profile', 'openid'])

# Abre un navegador para que el usuario elija la cuenta de google con la que autenticarse
# y devuelve un objeto GoogleUser con la info del usuario autenticado
def get_google_user() -> GoogleUser:
    flow.run_local_server()
    credentials = flow.credentials

    user_info_service = build('oauth2', 'v2', credentials=credentials)
    user_info = user_info_service.userinfo().get().execute()

    return GoogleUser.from_dict(user_info)
