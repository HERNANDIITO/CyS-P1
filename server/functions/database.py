import sqlite3
import os

def start():
    global cursor, database

    database = sqlite3.connect(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data\\database.db'), check_same_thread=False)
    cursor = database.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
        userId INTEGER PRIMARY KEY,
        user string, 
        password string,
        salt string,
        publicRSA string,
        privateRSA string,
        email string
    )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS files (
        fileId string,
        userId string,
        fileName string,
        encryptedFile string,
        AESKey string,
        publicRSA string,
        privateRSA string,
        date string,
        fileType string
    )""")

def merge_dicts(*dicts):
    res = {}
    for dict in dicts:
        for key in dict:
            res[key] = dict[key]
    return res

def get_keys(data, format, plus):
    keys_str = ""
    for key in data:
        keys_str = keys_str == "" and format.format(key, key) or keys_str + plus + format.format(key, key)
    return keys_str

def get_all_data(table):
    cursor.execute(f"SELECT * FROM {table}")
    data = cursor.fetchall()
    return data

# get_data("tabla", {"id": msg.author.id})
def get_data(table, data): 
    keys_str = get_keys(data, "{0}=:{1}", ", ")
    cursor.execute("SELECT * FROM {0} WHERE {1}".format(table, keys_str), data)
    data = cursor.fetchall()
    return len(data) > 0 and data[0] or None

# remove_data("tabla", {"key": args[0]})
def remove_data(table, data):
    keys_str = get_keys(data, "{0}=:{1}", ", ")
    cursor.execute("DELETE FROM {0} WHERE {1}".format(table, keys_str), data)
    database.commit()

# update_data("tabla", {"cookies": moodle_session, 'domain': domain}, {"id": msg.author.id})
def update_data(table, update, filter):
    update_str = get_keys(update, "{0}=:{1}", ", ")
    filter_str = get_keys(filter, "{0}=:{1}", " , ")
    cursor.execute("UPDATE {0} SET {1} WHERE {2}".format(table, update_str, filter_str), merge_dicts(update, filter))
    database.commit()

# insert_data("tabla", {"id": msg.author.id})
def insert_data(table, data):
    keys_str = get_keys(data, ":{0}", ", ")
    cursor.execute("INSERT INTO {0} VALUES ({1})".format(table, keys_str), data)
    database.commit()

def prueba_insert_data(table, data):
    fields = get_keys(data, "{0}", ", ")
    keys_str = get_keys(data, ":{0}", ", ")
    cursor.execute("INSERT INTO {0} ({1}) VALUES ({2})".format(table, fields, keys_str), data)
    database.commit()

def check_input(input):
    try: int(input)
    except: return True
    return False

def index_exists(ind, list):
    try: list[ind]
    except: return False
    return True