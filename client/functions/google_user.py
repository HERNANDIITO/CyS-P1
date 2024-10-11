from typing import Dict
from dataclasses import dataclass

# Es una dataclass ya que solo almacena info de un usuario autenticado con Google
@dataclass
class GoogleUser:
    id: str
    email: str
    verified_email: bool
    # Los campos con tipo str|None son opcionales. Pueden o no estar en la info del usuario
    name: str|None # Nombre completo
    given_name: str|None # Nombre
    family_name: str|None # Apellidos
    picture: str # Enlace a la foto de perfil
    
    # Funcion para obtener un GoogleUser a partir de un diccionario
    @staticmethod
    def from_dict(obj: Dict) -> 'GoogleUser':
        _id = str(obj.get("id"))
        _email = str(obj.get("email"))
        _verified_email = bool(obj.get("verified_email"))
        _name = str(obj.get("name")) if "name" in obj else None
        _given_name = str(obj.get("given_name")) if "given_name" in obj else None
        _family_name = str(obj.get("family_name")) if "family_name" in obj else None
        _picture = str(obj.get("picture"))
        return GoogleUser(_id, _email, _verified_email, _name, _given_name, _family_name, _picture)
