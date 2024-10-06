from functions import database as db
from functions.user import User

db.start()

User.createUser("Pablo", "123", "salty salty", "rsapub", "privrsa", "phg21")
User.createUser("lAURA", "123", "salty salty", "rsapub", "privrsa", "lsc82")