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
    - result.body:
        · userId: ID del usuario
    '''

    # Se leen los parametros del body
    input_json = request.get_json(force=True)

    # Se consume la función de clase para crear un usuario
    result = User.register(input_json["user"], input_json["password"], input_json["email"], input_json["publicRSA"], input_json["privateRSA"])

    # Se formatea el objeto tipo result como json y se devuelve como resultado de la peticion
    return json.loads(result.jsonSelf())

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
        - publicRSA: RSA Publico
    '''

    # Se leen los parametros del body
    input_json = request.get_json(force=True)

    # Se consume la función de clase para crear un usuario
    result = User.login(input_json["email"], input_json["password"])

    # Se formatea el objeto tipo result como json y se devuelve como resultado de la peticion
    return json.loads(result.jsonSelf())

@app.post("/users/update-keys")
def updateKeys():
    '''
    Servicio para modificar las keys tras el registro.
    Parámetros en el body de la petición:
    - userID: str
    - privateRSA: str
    - publicRSA: str

    return Result
    - result.msg: mensaje de contexto
    - result.code: codigo de error http
    - result.status: si ha sido realizada la petición o no
    - result.body:  
        · privateRSA: RSA Privado
        · publicRSA: RSA Publico
    '''

    # Se leen los parametros del body
    input_json = request.get_json(force=True)

    # Se consume la función de clase para crear un usuario
    user = User(input_json["userID"])
    
    result = user.modifyKeys( privateRSA = input_json["privateRSA"], publicRSA = input_json["publicRSA"])

    # Se formatea el objeto tipo result como json y se devuelve como resultado de la peticion
    return json.loads(result.jsonSelf())

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
    return json.loads(result.jsonSelf())

@app.post('/upload')
def uploadFile():
    '''
    Servicio de subida de ficheros
    Parámetros en el body de la petición:
    - fichero: file (ver test del cliente)
    - aesKey
    - userId
    - fileType

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
        result = File.upload(file, app.config['UPLOAD_FOLDER'], input_json['aesKey'], input_json['userId'], input_json['fileType'])
        
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

@app.get('/get-file-info/<path:file_id>')
def get_file_info(file_id):
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
    return json.loads(File.getFileData(file_id).jsonSelf())

@app.delete('/files')
def delete():
    '''
    Servicio de eliminación de ficheros
    '''

    input_json = request.get_json(force=True)
    file = File(input_json["fileId"])
    result = file.delete()
    return json.loads(result.jsonSelf())

@app.get('/files/<path:user_id>')
def getFiles(user_id):
    '''
    Servicio de obtencion de ficheros de un usuario
    Parámetros en el body de la petición:
    - user_id: id del usuario

    return Response
    - result.msg: mensaje de contexto
    - result.code: codigo de error http
    - result.status: si ha sido realizada la petición o no
    - result.body: lista de ficheros
    '''
    # Ruta de los ficheros subidos, de donde se obtiene el fichero a descargar

    user = User(user_id)
    return json.loads(user.getFiles().jsonSelf())

app.run()