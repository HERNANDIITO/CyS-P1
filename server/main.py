import os
from flask import Flask, request, jsonify
from flask_compress import Compress
from functions.user import User
from functions.result import Result
from functions.file import File
from functions.shared_file import SharedFile
from waitress import serve
from functions.debug import printMoment

app = Flask(__name__)
Compress(app)
app.config['UPLOAD_FOLDER'] =  os.path.join(app.root_path, 'data', 'uploads')

@app.get("/")
def landingPage():
    return """
        <script src="https://cdn.jsdelivr.net/npm/sweetalert2@11"></script>
        <style>
            body {
            margin: 0;
            background-color: #000;
        }

        .container {
            background-color: rgba(255, 255, 255, 0.85);
            margin: 50px 10%;
            padding: 3rem;
            position: relative;
            z-index: 1;
        }

        #canv {
            position: fixed;
            top: 0;
            left: 0;
        }
        @keyframes grow {
            0% {
                transform: scale(1);
            }
            50% {
                transform: scale(2.25);
            }
            100% {
                transform: scale(1);
            }
        }
        </style>
        <canvas id="canv"></canvas>
        <div class="container">
        <head>
            <title>Asegurados</title>
        </head>
        <h1 style='
            background-color: #601E88;
            color: #ffffff;
            padding: 5px 10px
        '>Asegurados</h1>
        <h2>Servidor de Asegurados.</h2>
        <p>Creado por: </p>
        <ul>
            <li>David González  </li>
            <li>Pablo Hernández </li>
            <li>Marcos Ruiz     </li>
            <li>Laura Saval     </li>
            <li>Javier Silva    </li>
        </ul>
        <audio id="epicMusic" src="https://marcosruizrubio.com/multimedia/cyberpunk.mp3" autoplay></audio>
        <button id="downloadBtn" style="animation:grow 2s linear infinite;">Descargar</button>
        </div>
        
        <script>
            Swal.fire('Bienvenido a Asegurados, el servicio más seguro de la historia 😈').then(() => document.getElementById('epicMusic').play());
            document.getElementById('downloadBtn').addEventListener('click', (e) => {
                Swal.fire('Esto debería descargar el exe');
            });
            
            const canvas = document.getElementById('canv');
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
            const ctx = canvas.getContext('2d');
            let cols = Math.floor(window.innerWidth / 20) + 1;
            let ypos = Array(cols).fill(0);

            ctx.fillStyle = '#000';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            function matrix () {
                const w = window.innerWidth;
                const h = window.innerHeight;
                
                if (canvas.width !== w) {
                    canvas.width = w;
                    cols = Math.floor(window.innerWidth / 20) + 1;
                    ypos = Array(cols).fill(0);
                }
                if (canvas.height !== h) {
                    canvas.height = h;
                }

                ctx.fillStyle = '#0001';
                ctx.fillRect(0, 0, w, h);

                ctx.fillStyle = '#0f0';
                ctx.font = '15pt monospace';

                ypos.forEach((y, ind) => {
                    const text = String.fromCharCode(Math.random() * 128);
                    const x = ind * 20;
                    ctx.fillText(text, x, y);
                    if (y > 100 + Math.random() * 10000) ypos[ind] = 0;
                    else ypos[ind] = y + 20;
                });
            }

            setInterval(matrix, 50);
        </script>
    """

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
    - salt: str
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
    result = User.register(input_json["user"], input_json["password"], input_json["email"], input_json["publicRSA"], input_json["privateRSA"], input_json["salt"])

    # Se formatea el objeto tipo result como json y se devuelve como resultado de la peticion
    return jsonify(result.jsonSelf())

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
    return jsonify(result.jsonSelf())

@app.post("/users/getSaltByEmail")
def getSaltByEmail():
    '''
    Servicio para recuperar el salt del servidor.
    Parámetros en el body de la petición:
    - email: str

    return Result
    - result.msg: mensaje de contexto
    - result.code: codigo de error http
    - result.status: si ha sido realizada la petición o no
    - result.body:  
        · salt: salt del usuario
    '''

    # Se leen los parametros del body
    input_json = request.get_json(force=True)

    # Se consume la función de clase para crear un usuario
    user = User(email=input_json["email"])
    
    if ( user.userId == -1 ):
        result = Result(400, "El usuario no existe", False)
        return(jsonify(result.jsonSelf()))
    
    result = user.getSalt()

    # Se formatea el objeto tipo result como json y se devuelve como resultado de la peticion
    return jsonify(result.jsonSelf())

@app.get("/users/shareParamsByEmail/<path:email>")
def shareParamsByEmail(email):
    '''
    Servicio para recuperar el salt del servidor.
    Parámetros en el body de la petición:
    - email: str

    return Result
    - result.msg: mensaje de contexto
    - result.code: codigo de error http
    - result.status: si ha sido realizada la petición o no
    - result.body:  
        · userID: id del usuario
        · publicRSA: publicRSA del usuario
    '''

    # Se consume la función de clase para crear un usuario
    user = User(email=email)
    
    if ( user.userId == -1 ):
        result = Result(400, "El usuario no existe", False)
        return(jsonify(result.jsonSelf()))
    
    result = user.getID()

    # Se formatea el objeto tipo result como json y se devuelve como resultado de la peticion
    return jsonify(result.jsonSelf())

@app.get("/users/shareParamsByID/<path:userID>")
def shareParamsByID(userID):
    '''
    Servicio para recuperar el salt del servidor.
    Parámetros en el body de la petición:
    - userID: str

    return Result
    - result.msg: mensaje de contexto
    - result.code: codigo de error http
    - result.status: si ha sido realizada la petición o no
    - result.body:  
        · userID: id del usuario
        · publicRSA: publicRSA del usuario
    '''

    # Se consume la función de clase para crear un usuario
    user = User(userId=userID)
    
    if ( user.userId == -1 ):
        result = Result(400, "El usuario no existe", False)
        return(jsonify(result.jsonSelf()))
    
    result = user.getID()

    # Se formatea el objeto tipo result como json y se devuelve como resultado de la peticion
    return jsonify(result.jsonSelf())

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
    return jsonify(result.jsonSelf())

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
    return jsonify(result.jsonSelf())

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
    return jsonify(str(result))

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
    return jsonify(File.getFileData(file_id).jsonSelf())

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
    return jsonify(result.jsonSelf())

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
    return jsonify(user.getFiles().jsonSelf())

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
    return jsonify(user.getPublicRsa().jsonSelf())

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
    return jsonify(user.getSharedFilesOfUser().jsonSelf())

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
    return jsonify(user.getSharedFilesToUser().jsonSelf())

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
    file_to_share = File(input_json["file_id"])
    return jsonify(SharedFile.share(file_to_share, input_json["reciever_id"], input_json["key"]).jsonSelf())

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
    return jsonify(shared_file.delete().jsonSelf())

@app.delete('/shared-user')
def deleteSharedUser():
    '''
    Servicio de eliminación de ficheros compartidos
    
    Parámetros en el body de la petición:
    - reciever_email: email del usuario con el que se desea dejar de compartir
    - file_id: id que se desea dejar de compartir
    
    return Response
    - result.msg: mensaje de contexto
    - result.code: codigo de error http
    - result.status: si ha sido realizada la petición o no
    - result.body: el fichero compartido borrado
    '''
    input_json = request.get_json(force=True)
    return jsonify(SharedFile.deleteSharedUser(input_json["reciever_email"], input_json["file_id"]).jsonSelf())

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

    result = SharedFile.getUsersSharedTo(file_id).jsonSelf()
    return jsonify(result)

@app.get('/get-shared-info/<path:sharingId>')
def getSharedInfo(sharingId):
    '''
    Servicio de obtencion de fila de la tabla de comparticion dada la ID del archivo
    - sharingId: id de la comparticion

    return Response
    - result.msg: mensaje de contexto
    - result.code: codigo de error http
    - result.status: si ha sido realizada la petición o no
    - result.body:
        · sharingId
        · sharedFileId
        · transmitterId
        · recieverId
        · key
    '''
    
    sharedFile = SharedFile(sharingId = sharingId)
    
    if ( sharedFile.sharingId == -1):
        result = Result(400, "El archivo no existe", False)
        return(jsonify(result.jsonSelf()))

    result = Result(200, "Archivo enviado con éxito", True, { "file": sharedFile.getFileDataJSON() }) 
    return jsonify(result.jsonSelf())

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
    return jsonify(user.changeData(input_json["user"], input_json["email"]).jsonSelf())

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
    return jsonify(user.changePassword(input_json['password'], input_json['oldPassword'], input_json['publicRSA'], input_json['privateRSA']).jsonSelf())

@app.get('/otp-url/<path:user_id>')
def getOtpUrl(user_id):
    '''
    Servicio de obtencion de la URl para el qr de doble factor de autenticacion de un usuario
    Parámetros en el body de la petición:
    - user_id: id del usuario

    return Response
    - result.msg: mensaje de contexto
    - result.code: codigo de error http
    - result.status: si ha sido realizada la petición o no
    - result.body: url para el qr de doble factor de autenticacion
    '''
    user = User(user_id)
    return jsonify(user.getOtpUrl().jsonSelf())

@app.post("/users/check-otp")
def checkUserOtpCode():
    '''
    Servicio para comprobar el codigo OTP del doble factor de autenticacion.
    Parámetros en el body de la petición:
    - user_id: str
    - otp_code: str

    return Result
    - result.msg: mensaje de contexto
    - result.code: codigo de error http
    - result.status: si ha sido realizada la petición o no
    - result.body: si el codigo es correcto o no
    '''

    # Se leen los parametros del body
    input_json = request.get_json(force=True)
    
    user = User(input_json["user_id"])
    
    return jsonify(user.checkOtpCode(input_json["otp_code"]).jsonSelf())

# Ejecuta el app.run() solo si se ejecuta con "python main.py". Hace falta para que funcione en el servidor real
if __name__ == "__main__":
    # serve(app, host='0.0.0.0', port=5000, threads=4)
    app.run(host='0.0.0.0', port=5000)