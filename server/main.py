import os
from flask import Flask, request
from functions.user import User
from functions.result import Result
import json
from functions.file import File

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] =  os.path.join(app.root_path, 'data', 'uploads')

@app.put("/users/register")
def registerUserPassword():
    # Esto de aquí abajo de un docstirng, es como un comentario multilinea para comentar sobre una funcion
    # Si le haceis hover sobre registerUserPassword lo veréis como tooltip (deberia ser sobre la funcion de abajo pero los decoradores lo vuelven un poco loco).

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

    # Se leen los parametros del body
    input_json = request.get_json(force=True)

    # Se consume la función de clase para crear un usuario
    result = User.register(input_json["user"], input_json["password"], input_json["email"], input_json["publicRSA"], input_json["privateRSA"])

    # Se formatea el objeto tipo result como json y se devuelve como resultado de la peticion
    return json.loads(str(result))

@app.post("/users/login")
def loginUserPassword():
    '''
    Servicio para iniciar sesión como usuario.
    Parámetros en el body de la petición:
    - email: str
    - password: str

    return Result
    - result.msg: mensaje de contexto
    - result.code: codigo de error http
    - result.status: si ha sido realizada la petición o no
    - result.body:  
        · userId: ID del suaurio
        · privateRSA: RSA Privado
    '''

    # Se leen los parametros del body
    input_json = request.get_json(force=True)

    # Se consume la función de clase para crear un usuario
    result = User.login(input_json["email"], input_json["password"])

    # Se formatea el objeto tipo result como json y se devuelve como resultado de la peticion
    return json.loads(str(result))

@app.post("/users/login-google")
def loginGoogle():
    '''
    Servicio para iniciar sesión como usuario.
    Parámetros en el body de la petición:
    - idToken: str

    return Result
    - result.msg: mensaje de contexto
    - result.code: codigo de error http
    - result.status: si ha sido realizada la petición o no
    - result.body:  
        · userId: ID del usuario
        · privateRSA: RSA Privado
    '''

    # Se leen los parametros del body
    input_json = request.get_json(force=True)

    # Se consume la función de clase para crear un usuario
    result = User.loginGoogle(input_json["idToken"])

    # Se formatea el objeto tipo result como json y se devuelve como resultado de la peticion
    return json.loads(str(result))

@app.post('/upload')
def uploadFile():
    '''
    Servicio de subida de ficheros
    Parámetros en el body de la petición:
    - fichero: file (ver test del cliente)
    - aeskey
    - publicRSA
    - privateRSA
    - userId

    return Result
    - result.msg: mensaje de contexto
    - result.code: codigo de error http
    - result.status: si ha sido realizada la petición o no
    '''
    result: Result
    # Comprueba que se haya subido un fichero con el nombre 'fichero'
    if 'fichero' not in request.files:
        result = Result(400, "No hay un fichero con el nombre 'fichero' en la petición", False)
    
    file = request.files['fichero']
    # Comprueba que se haya seleccionado un fichero
    if file.filename == '':
        result = Result(400, "No se ha enviado ningún fichero", False)
    
    if file:
        input_json = request.form.to_dict()
        result = File.upload(file, app.config['UPLOAD_FOLDER'], input_json['aesKey'], input_json['publicRSA'], input_json['privateRSA'], input_json['userId'])
        
    #file.close() 
    return json.loads(str(result))

# TODO: Implementar algo para comprobar autenticidad del usuario (se podria usar tokens)
@app.get('/download/<path:file_id>')
def download(file_id):
    '''
    Servicio de bajada de ficheros
    Parámetros en el body de la petición:
    - file_id: id del fichero a descargar

    return Response
    - result.msg: mensaje de contexto
    - result.code: codigo de error http
    - result.status: si ha sido realizada la petición o no
    - result.body: el fichero
    '''
    # Ruta de los ficheros subidos, de donde se obtiene el fichero a descargar
    uploads_path = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    # Devuelve el fichero con el nombre especificado
    return File.download(uploads_path, file_id)