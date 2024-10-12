import os
from flask import Flask, request, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploaded_files'

# Servicio de subida de ficheros
@app.post('/upload-test')
def upload_file():
    # Comprueba que se haya subido un fichero con el nombre 'fichero'
    if 'fichero' not in request.files:
        return 'No hay un fichero con el nombre "file" en la petición'
    
    file = request.files['fichero']
    # Comprueba que se haya seleccionado un fichero
    if file.filename == '':
        return 'No se ha seleccionado un fichero'
    
    if file:
        # secure_filename filtra el nombre del fichero para evitar ataques
        filename = secure_filename(file.filename)
        # Guarda fichero en la carpeta especificada en UPLOAD_FOLDER
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'Sí.'

# Servicio de descarga de ficheros.Recibe un parametro en la ruta con el nombre del fichero
@app.get('/download-test/<path:filename>')
def download(filename):
    # Ruta de los ficheros subidos, de donde se obtiene el fichero a descargar
    uploads = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    # Devuelve el fichero con el nombre especificado
    return send_from_directory(uploads, filename)