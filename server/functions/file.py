import database

class user:
    def __init__(self, userId):
        database.get_data("users", {"userId": userId})

