from flask import Flask, url_for, request
from flask import render_template
from pymongo import MongoClient
client = MongoClient()
# from flask.ext.mongoengine import MongoEngine
# from mongoengine import connect

app = Flask(__name__)
# app.config["MONGODB_SETTINGS"] = {'DB': "Recipes"}
# app.config["SECRET_KEY"] = "KeepThisS3cr3t"

# connect('Recipes')

db = client['Recipes']

@app.route('/')
def index():
	#check for login and populate mainpage

	return render_template('design_homepage.html')

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
	return render_template('hello.html', name=None)

@app.route('/add_recipe/')
def addRecipe():
	return render_template('design_recipe.html')

@app.route('/recipe/')
#@app.route('/recipe/<name>/<user>')
def viewRecipe():
	#give name for recipe, find in database
	directions = "In a small bowl, dissolve yeast in 1/4 cup warm milk. Let stand until creamy, about 10 minutes.\n\nIn a large bowl, whisk together the egg yolks, 1/4 cup of the warm milk and the melted butter. Stir in the yeast mixture, sugar, salt and vanilla. Stir in the remaining 2 1/2 cups milk alternately with the flour, ending with the flour. Beat the egg whites until they form soft peaks; fold into the batter. Cover the bowl tightly with plastic wrap. Let rise in a warm place until doubled in volume, about 1 hour.\n\nPreheat the waffle iron. Brush with oil and spoon about 1/2 cup (or as recommended by manufacturer) onto center of iron. Close the lid and bake until it stops steaming and the waffle is golden brown. Serve immediately or keep warm in 200 degree oven."
	
	return render_template('design_recipe.html',name="Belgium Waffles",preptime="1 hr 35 min",amount="one dozen waffles",dir=directions)

@app.route('/recipe/ice/')
def makeIce():
	collection = db.recipe
	ice = collection.find_one({"title": "ICE"})
	#ice = db.find()
	print ice['title']
	#if(ice != null):
	return render_template('design_recipe.html',name=ice['title'],preptime="1 hr 35 min",amount="one dozen waffles",dir=ice['instructions'] )
	#else:
	 #	return render_template('hello.html', name=None)
@app.route('/shopping/')
def shopping():
	return render_template('design_shopping_list.html')

@app.route('/my_recipes/')
def myRecipe():
	return render_template('design_myRecipes.html')


if __name__ == '__main__':
	app.run(debug=True)