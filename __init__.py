from flask import Flask, url_for, request
from flask import render_template
from flask.ext.login import LoginManager
from flask.ext.mongoengine import MongoEngine

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = {'DB': "Recipes"}
app.config["SECRET_KEY"] = "KeepThisS3cr3t"

db = MongoEngine(app)
loginManager = LoginManager()
loginManager.init_app(app)

def register_blueprints(app):
	from DinnerTrackingGuide.views import users
	app.register_blueprint(users)

register_blueprints(app)

@app.route('/')
@app.route('/index')
def index():
	#check for login and populate mainpage
	#return render_template('design_homepage.html')
	return render_template('design_homepage_copy.html')

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
	return render_template('base.html', name=None)
#return render_template('design_homepage.html')

@app.route('/add_recipe/')
def addRecipe():
	return render_template('design_recipe.html')

@app.route('/recipe/')
#@app.route('/recipe/<name>/<user>')
def viewRecipe():
	#give name for recipe, find in database
	ingredients = [
				   "1 (.25 ounce) package active dry yeast",
				   "4 cups warm milk (110 degrees F/45 degrees C)",
				   "3 eggs",
				   "3/4 cup butter, melted and cooled to lukewarm",
				   "1 1/2 teaspoons salt",
				   "2 teaspoons vanilla extract",
				   "4 cups all-purpose flour"
			 ]
	
	directions = [
					"In a small bowl, dissolve yeast in 1/4 cup warm milk. Let stand until creamy, about 10 minutes.",
					" In a large bowl, whisk together the egg yolks, 1/4 cup of the warm milk and the melted butter. Stir in the yeast mixture, sugar, salt and vanilla. Stir in the remaining 2 1/2 cups milk alternately with the flour, ending with the flour. Beat the egg whites until they form soft peaks; fold into the batter. Cover the bowl tightly with plastic wrap. Let rise in a warm place until doubled in volume, about 1 hour.",
						"Preheat the waffle iron. Brush with oil and spoon about 1/2 cup (or as recommended by manufacturer) onto center of iron. Close the lid and bake until it stops steaming and the waffle is golden brown. Serve immediately or keep warm in 200 degree oven."
	]
	
#	return render_template('design_recipe.html',name="Belgium Waffles",preptime="1 hr 35 min",amount="one dozen waffles",ingr=ingredients,dir=directions)
#	return render_template('recipe.html',name="Belgium Waffles",preptime="1 hr 35 min",amount="one dozen waffles",ingr=ingredients,dir=directions)
	

@app.route('/recipe/ice/')
def makeIce():
	from models import Recipe
	collection = db.recipe.Objects
	ice = db.Recipes.find_one({"title": "ICE"})
	#ice = db.find()
	print ice['title']
	#if(ice != null):
	return render_template('design_recipe_new.html',name=ice['title'],preptime="1 hr 35 min",amount="one dozen waffles",dir=ice['instructions'] )
	#else:
	 #	return render_template('hello.html', name=None)

shoppingList = [
					"12 eggs",
					"2 gallons milk",
					"Cream Cheese",
					"3/4 C butter",
					"2 t lemon pepper",
					"3 T vanilla extract",
					"4 C all-purpose flour"
				]
@app.route('/shopping/')
def shopping():
	#return render_template('design_shopping_list.html', items=itmesForList)
	return render_template('shopping_list.html', items=shoppingList)

@app.route('/my_recipes/')
def myRecipe():
	#return render_template('design_myRecipes.html')
	return render_template('myRecipes.html')

@app.context_processor
def utility_processor():
	def addToShoppingList(ingredients):
		shoppingList.extend(ingredients)
		return '/shopping/'
	return dict(addToShoppingList=addToShoppingList)

if __name__ == '__main__':
	app.run(debug=True)

