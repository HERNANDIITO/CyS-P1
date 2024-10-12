from flask import Flask, request
from functions.user import User
from functions.result import Result
import json

app = Flask(__name__)

# Esto de aquí abajo de un docstirng, es como un comentario multilinea para comentar sobre una funcion
# Si le haceis hover sobre @app vereis este popup (deberia ser sobre la funcion de abajo pero los decoradores lo vuelven un poco loco).
'''
Servicio para registrar usuarios.
Parámetros en el body de la petición:
- user: str
- password: str
- email: str
- publicRSA: str
- privateRSA: str

return Result
- result.msg: mensaje de contexto
- result.code: codigo de error http
- result.status: si ha sido realizada la petición o no
'''
@app.put("/users/regsiter")
def registerUserPassword():
    # Se leen los parametros del body
    input_json = request.get_json(force=True)

    # Se consume la función de clase para crear un usuario
    result = User.register(input_json["user"], input_json["password"], input_json["email"])

    # Se formatea el objeto tipo result como json y se devuelve como resultado de la peticion
    return json.loads(str(result))

'''
Servicio para iniciar sesión como usuario.
Parámetros en el body de la petición:
- user: str
- password: str

return Result
- result.msg: mensaje de contexto
- result.code: codigo de error http
- result.status: si ha sido realizada la petición o no
- result.body: ID del suaurio
'''
@app.post("/users/login")
def loginUserPassword():
    # Se leen los parametros del body
    input_json = request.get_json(force=True)

    # Se consume la función de clase para crear un usuario
    result = User.login(input_json["user"], input_json["password"])

    # Se formatea el objeto tipo result como json y se devuelve como resultado de la peticion
    return json.loads(str(result))