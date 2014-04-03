from flask import Flask, url_for, request
from flask import render_template
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {'DB': "Recipies"}
app.config["SECRET_KEY"] = "KeepThisS3cr3t"

db = MongoEngine(app)

@app.route('/')
def index():
	return render_template('design_homepage.html')

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
	return render_template('hello.html', name=name)

@app.route('/add_recipe')
def addRecipe():
	return render_template('design_edit_recipe.html')

if __name__ == '__main__':
	app.run()