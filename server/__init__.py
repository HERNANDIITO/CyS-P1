from functions import database as db
from functions.user import User

db.start()

yoMismo = User.createUser(3, "Pablo", "1432")