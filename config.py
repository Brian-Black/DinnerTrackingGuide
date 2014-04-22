from flask import Flask

from flask.ext.mongoengine import MongoEngine
from mongoengine import connect
from mongoengine.connection import _get_db

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {'DB': "Recipes"}

db = MongoEngine(app)

#To drop the database
database = _get_db()
#database.connection.drop_database('Recipes')

# You must configure these 3 values from Google APIs console
# https://console.developers.google.com/project/apps~dinner-planner-cs360/apiui/credential
GOOGLE_CLIENT_ID = ''

GOOGLE_CLIENT_SECRET = ''
REDIRECT_URI = ''  # one of the Redirect URIs from Google APIs console

# generate with os.urandom(24) in a Python shell
SECRET_KEY = ''

app.secret_key = SECRET_KEY

