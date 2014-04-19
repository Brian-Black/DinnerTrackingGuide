from flask import Flask

from flask.ext.mongoengine import MongoEngine
from mongoengine import connect
from mongoengine.connection import _get_db

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {'DB': "Recipes"}

db = MongoEngine(app)

#To drop the database
database = _get_db()
database.connection.drop_database('Recipes')

# You must configure these 3 values from Google APIs console
# https://console.developers.google.com/project/apps~dinner-planner-cs360/apiui/credential
GOOGLE_CLIENT_ID = '318054669713-blfppvbs8d8n8t9sat3khkfd9fl3t18v.apps.googleusercontent.com'


GOOGLE_CLIENT_SECRET = 'CrPQqpJAh7JncCex1IXOAQn1'
REDIRECT_URI = '/index'  # one of the Redirect URIs from Google APIs console

# generate with os.urandom(24) in a Python shell
SECRET_KEY = '4)\xfb\t\xf4(>;\xca\xe1.\x8a\x86\x93\xb6}\x91@\xb9a\x8b\xde\x82\x15'

app.secret_key = SECRET_KEY

