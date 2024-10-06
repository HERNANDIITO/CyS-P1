# CyS-P1

## Estructura de carpetas Client

```
.
├── main.py                     # Inicia el programa
├── __init__.py                 # Init
├── __init__.py                 # Hace de raíz para el paquete y se ejecuta cuando se importa
├── requirements.txt            # Dependencias
├── functions                   # Carpeta contenedora de los módulos    
│   ├── __init__.py             # Init de functions
│   └── aesrsa.py               # Funciones relacionadas con AES + RSA
├── tests                       # Carpeta con pruebas varias
├── ui                          # Carpeta con pruebas varias
│   ├── __init__.py             # Init de ui
│   ├── imgs                    # Imágenes
│   ├── ui.py                   # Funciones de la interfaz
│   └── ui_login.py             # Funciones de la interfaz de login
├── keys                        # Carpeta con pruebas varias
│   ├── public_key.pem          # Contenedor de claves publicas (CLIENT SIDE)
│   └── private_key.pem         # Contenedor de claves privadas (CLIENT SIDE)
└── ...
```

## Estructura de carpetas Server

```
.
├── main.py             # Inicia el programa
├── __init__.py         # Hace de raíz para el paquete y se ejecuta cuando se importa
├── requirements.txt    # Dependencias
├── functions           # Carpeta contenedora de los módulos    
│   ├── database.py     # Gestor de la base de datos
│   ├── user.py         # Clase de los usuarios
│   └── file.py         # Clase de los ficheros
├── data                # Almacena datos server side
│   └── database.db     # Almacena la base de datos
├── tests               # Carpeta con pruebas varias
├── private_key.pem     # Contenedor de claves privadas (CLIENT SIDE)
├── public_key.pem      # Contenedor de claves publicas (CLIENT SIDE)
├── public_key.pem      # Dependencias
└── ...
```

## Normas de uso

Intentad editar el archivo `main.py` lo mínimo posible.
Todo lo que hagáis tiene que estar recogido en la carpeta `functions`.
En caso de necesitar más de un archivo para una misma cosa, cread una carpeta:


Intentad documentar todo con comentarios de este estilo:

```py
# get_data("tabla", {"id": msg.author.id})
def get_data(table, data): 
    keys_str = get_keys(data, "{0}=:{1}", ", ")
    cursor.execute("SELECT * FROM {0} WHERE {1}".format(table, keys_str), data)
    data = cursor.fetchall()
    return len(data) > 0 and data[0] or None
```

## Importar un paquete

```py
import functions.aesrsa
```
Esto se debe a que partimos del archivo `__init__` para hacer las rutas, por lo que la ruta desde ahí sería:
`functions/aesrsa.py` sustituimos la `/` por `.` y eliminamos extensiones.

## Dependencias

### Instalar/Actualizar rependencias

#### Cliente

`pip install -r ./client/requirements.txt`

#### Servidor

`pip install -r ./server/requirements.txt`

### Añadir dependencias

Es habitual que el proyecto vaya variando de dependencias, y como trabajamos en equipo es importante llevar un seguimiento de las mismas.
Para ello utilizaremos una librería de python
Para instalarla es tan simple como: `pip install pipreqs`
Una vez hecho esto, vais a la raíz del proyecto y escribis el siguiente comando:

#### Cliente

`pipreqs .\client --force`

#### Servidor

`pipreqs .\server --force`