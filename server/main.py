import os
from flask import Flask, request
from functions.user import User
from functions.result import Result
import json
from functions.file import File
from functions.shared_file import SharedFile

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
    - fileName
    - aesKey
    - userId
    - fileType
    - signature

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
        result = File.upload(file, app.config['UPLOAD_FOLDER'], input_json['aesKey'], input_json['userId'], input_json['fileType'], input_json['fileName'], input_json['signature'])
        
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
def deleteFile():
    '''
    Servicio de eliminación de ficheros
    
    Parámetros en el body de la petición:
    - file_id: id del fichero a descargar

    return Response
    - result.msg: mensaje de contexto
    - result.code: codigo de error http
    - result.status: si ha sido realizada la petición o no
    - result.body: el fichero
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

    user = User(user_id)
    return json.loads(user.getFiles().jsonSelf())

@app.get('/public-rsa/<path:user_id>')
def getPublicRsa(user_id):
    '''
    Servicio de obtencion de clave RSA publica de un usuario
    Parámetros en el body de la petición:
    - user_id: id del usuario

    return Response
    - result.msg: mensaje de contexto
    - result.code: codigo de error http
    - result.status: si ha sido realizada la petición o no
    - result.body: clave RSA publica del usuario
    '''

    user = User(user_id)
    return json.loads(user.getPublicRsa().jsonSelf())

@app.get('/shared-files-of/<path:user_id>')
def getSharedFilesOfUser(user_id):
    '''
    Servicio de obtencion de los archivos compartidos por un usuario
    Parámetros en el body de la petición:
    - user_id: id del usuario

    return Response
    - result.msg: mensaje de contexto
    - result.code: codigo de error http
    - result.status: si ha sido realizada la petición o no
    - result.body: archivos compartidos por el usuario
    '''

    user = User(user_id)
    return json.loads(user.getSharedFilesOfUser().jsonSelf())

@app.get('/shared-files-to/<path:user_id>')
def getSharedFilesToUser(user_id):
    '''
    Servicio de obtencion de los archivos compartidos a un usuario
    Parámetros en el body de la petición:
    - user_id: id del usuario

    return Response
    - result.msg: mensaje de contexto
    - result.code: codigo de error http
    - result.status: si ha sido realizada la petición o no
    - result.body: archivos compartidos al usuario
    '''

    user = User(user_id)
    return json.loads(user.getSharedFilesToUser().jsonSelf())

@app.post('/share-file')
def shareFile():
    '''
    Servicio de subida de ficheros
    Parámetros en el body de la petición:
    - file_id
    - reciever_id
    - key

    return Result
    - result.msg: mensaje de contexto
    - result.code: codigo de error http
    - result.status: si ha sido realizada la petición o no
    - result.body: los datos del fichero compartido
    '''
    
    input_json = request.get_json(force=True)
    file_to_share = File(input_json["fileId"])
    return json.loads(SharedFile.share(file_to_share, input_json["recieverId"], input_json["key"]).jsonSelf())

@app.delete('/shared-files')
def deleteSharedFile():
    '''
    Servicio de eliminación de ficheros compartidos
    
    Parámetros en el body de la petición:
    - sharing_id: id del fichero a descargar

    return Response
    - result.msg: mensaje de contexto
    - result.code: codigo de error http
    - result.status: si ha sido realizada la petición o no
    - result.body: el fichero compartido borrado
    '''

    input_json = request.get_json(force=True)
    shared_file = SharedFile(input_json["sharing_id"])
    return json.loads(shared_file.delete().jsonSelf())

@app.get('/users-shared-to/<path:file_id>')
def getUsersSharedTo(file_id):
    '''
    Servicio de obtencion de la lista de usuarios con los que 
    esta compartido un mismo archivo dada la ID del archivo
    - file_id: id del fichero

    return Response
    - result.msg: mensaje de contexto
    - result.code: codigo de error http
    - result.status: si ha sido realizada la petición o no
    - result.body: archivos compartidos por el usuario
    '''

    return json.loads(SharedFile.getUsersSharedTo(file_id).jsonSelf())

@app.post("/users/change-data/<path:user_id>")
def changeUserData(user_id):
    '''
    Servicio para cambiar datos de un usuario.
    Parámetros en el body de la petición:
    - user_id: str
    - user: str
    - email: str

    return Result
    - result.msg: mensaje de contexto
    - result.code: codigo de error http
    - result.status: si ha sido realizada la petición o no
    - result.body:  
        · user: Datos del usuario tras los cambios
    '''

    # Se leen los parametros del body
    input_json = request.get_json(force=True)

    user = User(user_id)
    return json.loads(user.changeData(input_json["user"], input_json["email"]).jsonSelf())

@app.post("/users/change-password/<path:user_id>")
def changeUserPassword(user_id):
    '''
    Servicio para cambiar contrasenya de un usuario.
    Parámetros en el body de la petición:
    - user_id: str
    - password: str
    - oldPassword: str
    - salt: str
    - publicRSA: str
    - privateRSA: str

    return Result
    - result.msg: mensaje de contexto
    - result.code: codigo de error http
    - result.status: si ha sido realizada la petición o no
    - result.body:  
        · user: Datos del usuario tras los cambios
    '''

    # Se leen los parametros del body
    input_json = request.get_json(force=True)

    user = User(user_id)
    return json.loads(user.changePassword(input_json['password'], input_json['oldPassword'], input_json['publicRSA'], input_json['privateRSA']).jsonSelf())


# Ejecuta el app.run() solo si se ejecuta con "python main.py". Hace falta para que funcione en el servidor real
if __name__ == "__main__":
    app.run()