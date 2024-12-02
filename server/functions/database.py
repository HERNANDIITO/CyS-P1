import sqlite3
import os

def start():
    '''
        Inicializa la base de datos.
        Crea la conexión con la base de datos.
        Se encarga de que las tablas existan.
    '''

    # Creamos dos variables globales para acceder desde cualquier lado del archivo
    global cursor, database

    # Les proporcionamos un valo:
    # database: guarda la conexción con la base de datos
    # cursor: guarda el cursor que ejectuta las sentencias
    database = sqlite3.connect(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'database.db'), check_same_thread=False)
    cursor = database.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Creamos la tabla users
    #   userId: clave primaria autoincremental
    #   user: nombre de usuario
    #   password: contraseña encriptada
    #   salt: salt
    #   publicRSA: clave rsa publica
    #   privateRSA: clave rsa privada
    #   email: email, clave alternativa

    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
        userId INTEGER PRIMARY KEY,
        user string, 
        password string,
        salt string,
        publicRSA string,
        privateRSA string,
        email string,
        otpSecret string
    )""")

    # Creamos la tabla files
    #   fileId: clave primaria autoincremental
    #   userId: Id del usuario dueño
    #   fileName: nombre de usuario
    #   encryptedFile: archivo cifrado
    #   signedFile: hash con SHA3-256 del archivo cifrado firmado con la clave RSA privada del usuario propietario
    #   AESKey: clave aes
    #   date: fecha de subida
    #   fileType: tipo de archivo 

    cursor.execute("""CREATE TABLE IF NOT EXISTS files (
        fileId INTEGER PRIMARY KEY,
        userId INTEGER,
        fileName string,
        encryptedFile string,
        AESKey string,
        date string,
        fileType string,
        signature string,
        FOREIGN KEY(userId) REFERENCES users(userId)
    )""")
    
    # Creamos la tabla sharedFiles
    #   sharingId: ID de la comparticion entre usuarios
    #   sharedFileId: ID del archivo a compartir
    #   transmitterId: ID del usuario que comparte
    #   recieverId: ID del usuario con quien se comparte
    #   key: Clave del archivo encriptado con la clave publica del reciever

    cursor.execute("""CREATE TABLE IF NOT EXISTS sharedFiles (
        sharingId INTEGER PRIMARY KEY,
        sharedFileId INTEGER,
        transmitterId INTEGER,
        recieverId INTEGER,
        key string,
        FOREIGN KEY(sharedFileId) REFERENCES files(fileId) ON DELETE CASCADE,
        FOREIGN KEY(transmitterId) REFERENCES users(userId),
        FOREIGN KEY(recieverId) REFERENCES users(userId)
    )""")

    # Indexar
    # -- Índice para la columna userId en la tabla files
    cursor.execute("""CREATE INDEX IF NOT EXISTS idx_userId_files ON files(userId)""")
    
    # -- Índice para las columnas transmitterId y sharedFileId en la tabla sharedFiles
    cursor.execute("""CREATE INDEX IF NOT EXISTS idx_transmitterId_sharedFileId ON sharedFiles(transmitterId, sharedFileId)""")
    
    # -- Índice para las columnas recieverId y sharedFileId en la tabla sharedFiles
    cursor.execute("""CREATE INDEX IF NOT EXISTS idx_recieverId_sharedFileId ON sharedFiles(recieverId, sharedFileId)""")
    
    database.commit()

def merge_dicts(*dicts):
    'Junta el array de diccionarios pasados por parámetros en un único diccionario'

    res = {}                        # Inicialización del diccionario resulatdo vacio
    for dict in dicts:              # Recorre todos los diccionarios de la lista de diccionarios proporcionada
        for key in dict:            # Navega por todas y cada una de las claves del diccionario
            res[key] = dict[key]    # Por cada clave del diccionario, añade una nueva al resultado con el mismo nombre y valor.
    return res

def get_keys(data, format, plus):
    'Coge todas las claves de un dict en un string unico formateado de una forma concreta indicada por parametro'
    keys_str = ""
    for key in data:
        keys_str = keys_str == "" and format.format(key, key) or keys_str + plus + format.format(key, key)
    return keys_str

def get_all_data(table):
    '''
        Devuelve toda la información de la tabla indicada por parámetro:
            Parametros:
                table (str): nombre de la tabla
            
            Return:
                Toda la información de la tabla
        
            Ejemplo:
                `get_all_data( "users" )`
                Devuelve todos los usuarios guardados en la tabla
    '''

    cursor.execute(f"SELECT * FROM {table}")
    data = cursor.fetchall()
    return data

def get_data(table, data): 
    '''
        Devuelve la información solicitada de la tabla indicada por parámetro:
            Parametros:
                table (str): nombre de la tabla
                data (dict): diccionario con el campo indicado
            
            Return:
                Información solicitada en array
        
            Ejemplo:
                `get_data( "users", { "userId": userId })`
                Devuelve toda la información del usuario indicado por parámetro
    '''

    keys_str = get_keys(data, "{0}=:{1}", ", ")
    cursor.execute("SELECT * FROM {0} WHERE {1}".format(table, keys_str), data)
    data = cursor.fetchall()
    return len(data) > 0 and data[0] or None

def get_data_with_map(table, data): 

    keys_str = get_keys(data, "{0}=:{1}", ", ")
    cursor.execute("SELECT * FROM {0} WHERE {1}".format(table, keys_str), data)
    data = cursor.fetchall()

    column_names = [desc[0] for desc in cursor.description]
    results = [dict(zip(column_names, row)) for row in data]

    return results if results else None

def get_file_data_map(table, data): 

    keys_str = get_keys(data, "{0}=:{1}", ", ")
    cursor.execute("SELECT fileId, userId, fileName, aesKey, fileType FROM {0} WHERE {1}".format(table, keys_str), data)
    data = cursor.fetchall()

    column_names = [desc[0] for desc in cursor.description]
    results = [dict(zip(column_names, row)) for row in data]

    return results if results else None

def get_shared_file_data_map(table, data): 

    keys_str = get_keys(data, "{0}=:{1}", ", ")
    cursor.execute("SELECT DISTINCT fileId, userId, fileName, AESKey, fileType, signature, sf.sharingId FROM {0} JOIN sharedFiles sf ON fileId = sf.sharedFileId WHERE {1}".format(table, keys_str), data)
    data = cursor.fetchall()

    column_names = [desc[0] for desc in cursor.description]
    results = [dict(zip(column_names, row)) for row in data]

    return results if results else None
    

def remove_data(table, data):
    '''
        Eilimna la información solicitada de la tabla indicada por parámetro:
            Parametros:
                table (str): nombre de la tabla
                data (dict): diccionario con el campo indicado
            
            Return:
                Nada
        
            Ejemplo:
                `remove_data( "users", { "userId": userId })`
                Elimina toda la información del usuario indicado por parámetro
    '''
        
    keys_str = get_keys(data, "{0}=:{1}", ", ")
    cursor.execute("DELETE FROM {0} WHERE {1}".format(table, keys_str), data)
    database.commit()

def update_data(table, update, filter):
    '''
        Acgtualiza la información solicitada de la tabla indicada por parámetro:
            Parametros:
                table (str): nombre de la tabla
                update (dict): campos a modificar
                filter (dict): fila a modificar
            
            Return:
                Nada
        
            Ejemplo:
                `update_data( "users", { "user": "nombreNuevo" }, { "userId": userId })`
                Actualiza la fila indicada con la información proporcionada por parámetro
    '''
    update_str = get_keys(update, "{0}=:{1}", ", ")
    filter_str = get_keys(filter, "{0}=:{1}", " , ")
    cursor.execute("UPDATE {0} SET {1} WHERE {2}".format(table, update_str, filter_str), merge_dicts(update, filter))
    database.commit()

def insert_data(table, data):
    '''
        Insertar la información solicitada de la tabla indicada por parámetro:
            Parametros:
                table (str): nombre de la tabla
                data (dict): campos de la fila
            
            Return:
                Nada
        
            Ejemplo:
                `update_data( "users", { "userId": userId })`
                Actualiza la fila indicada con la información proporcionada por parámetro
    '''
    keys_str = get_keys(data, ":{0}", ", ")
    print("Las keyu7s: ")
    cursor.execute("INSERT INTO {0} VALUES ({1})".format(table, keys_str), data)
    database.commit()