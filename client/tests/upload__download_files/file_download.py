import requests

# Envia petición GET para descargar un fichero
r = requests.get('http://localhost:5000/download-test/imgForDownload.png')

# Guarda el contenido de la respuesta en el fichero downloadedImage.png
open('downloadedImage.png', 'wb').write(r.content)