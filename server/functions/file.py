import database

class File:
    def __init__(self, userId):
        database.get_data("users", {"userId": userId})

