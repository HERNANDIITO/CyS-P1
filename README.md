# CyS-P1

## Estructura de carpetas

```
.
├── main.py             # Inicia el programa
├── readme.md           # Este archivo
├── info.md             # Listado de documentacion e informacion varia
├── requirements.txt    # Dependencias
├── functions           # Carpeta contenedora de los módulos    
│   ├── database.py     # Gestor de la base de datos
│   ├── rsa.py          # Funciones relacionadas con RSA
│   ├── database.py     # Gestor de la base de datos
│   ├── ui.py           # Funciones de la interfaz
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
