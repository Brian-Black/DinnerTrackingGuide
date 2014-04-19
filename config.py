from flask import Flask

from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {'DB': "Recipes"}

db = MongoEngine(app)

# You must configure these 3 values from Google APIs console
# https://console.developers.google.com/project/apps~dinner-planner-cs360/apiui/credential
GOOGLE_CLIENT_ID = '318054669713-blfppvbs8d8n8t9sat3khkfd9fl3t18v.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = 'CrPQqpJAh7JncCex1IXOAQn1'
REDIRECT_URI = '/index'  # one of the Redirect URIs from Google APIs console

# generate with os.urandom(24) in a Python shell
SECRET_KEY = '{\x88\xcc\x03v\xe0p\xee\xb4EV\x04\xe0\x14\xfc\x9c(m\xabD\xbf\xff;3'
app.secret_key = SECRET_KEY

