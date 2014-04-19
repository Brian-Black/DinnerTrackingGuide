from flask import Flask, url_for, request, render_template, Blueprint
from flask.ext.login import login_required, current_user
from flask import Flask, url_for, request
from flask import render_template
from flask.ext.login import LoginManager
from flask.ext.mongoengine import MongoEngine
from config import app, db
from authentication import login_manager

def register_blueprints(app):
	from DinnerTrackingGuide.views import users
	app.register_blueprint(users)

register_blueprints(app)

# # HOMEPAGE
# @app.route('/')
# @app.route('/index')
# def index():
# 	login = False
# 	name = None
# 	if current_user.is_authenticated():
# 		login = True 
# 		if current_user.username:
# 			name = current_user.username

# 	all_the_recipes = [
# 						"Belgium Waffles",
# 						"Blueberry Muffins"
# 					]	
# 	return render_template('homepage.html', allrecipes=all_the_recipes)

# # HELLO (does this actually do anything?)
# @app.route('/hello/')
# @app.route('/hello/<name>')
# def hello(name=None):
# 	return render_template('base.html', name=None)

# # ADD_RECIPE - do we need this anymore?
# @app.route('/add_recipe/')
# def addRecipe():
# 	return render_template('design_recipe.html')

# # RECIPE
# @app.route('/recipe/')
# #@app.route('/recipe/<name>/<user>')
# def viewRecipe():
# 	#give name for recipe, find in database
# 	ingredients = [
# 				   "1 (.25 ounce) package active dry yeast",
# 				   "4 cups warm milk (110 degrees F/45 degrees C)",
# 				   "3 eggs",
# 				   "3/4 cup butter, melted and cooled to lukewarm",
# 				   "1 1/2 teaspoons salt",
# 				   "2 teaspoons vanilla extract",
# 				   "4 cups all-purpose flour"
# 				   ]
		
# 	directions = [
# 					"In a small bowl, dissolve yeast in 1/4 cup warm milk. Let stand until creamy, about 10 minutes.",
# 					" In a large bowl, whisk together the egg yolks, 1/4 cup of the warm milk and the melted butter. Stir in the yeast mixture, sugar, salt and vanilla. Stir in the remaining 2 1/2 cups milk alternately with the flour, ending with the flour. Beat the egg whites until they form soft peaks; fold into the batter. Cover the bowl tightly with plastic wrap. Let rise in a warm place until doubled in volume, about 1 hour.",
# 						"Preheat the waffle iron. Brush with oil and spoon about 1/2 cup (or as recommended by manufacturer) onto center of iron. Close the lid and bake until it stops steaming and the waffle is golden brown. Serve immediately or keep warm in 200 degree oven."
# 	]
	
# #	return render_template('design_recipe.html',name="Belgium Waffles",preptime="1 hr 35 min",amount="one dozen waffles",ingr=ingredients,dir=directions)
# #	return render_template('recipe.html',name="Belgium Waffles",preptime="1 hr 35 min",amount="one dozen waffles",ingr=ingredients,dir=directions)
	

# # WHAT DOES THIS EVEN DO???
# @app.route('/recipe/ice/')
# def makeIce():
# 	from models import Recipe
# 	collection = db.recipe.Objects
# 	ice = db.Recipes.find_one({"title": "ICE"})
# 	print ice['title']
# 	return render_template('design_recipe_new.html',name=ice['title'],preptime="1 hr 35 min",amount="one dozen waffles",dir=ice['instructions'] )

# SHOPPING_LIST
shoppingList = []
@app.route('/shopping/')
def shopping():
	#return render_template('design_shopping_list.html', items=itmesForList)
	return render_template('shopping_list.html', items=shoppingList)

# # MY_RECIPES
# @app.route('/my_recipes/')
# @login_required
# def myRecipe():
# 	all_the_recipes = [
# 					   "Belgium Waffles"
# 					   ]	
# 	return render_template('myRecipes.html', myrecipes=all_the_recipes)

# add ingredients to shopping list
@app.context_processor
def utility_processor():
	def addToShoppingList(ingredients):
		shoppingList.extend(ingredients)
		return '/shopping/'
	return dict(addToShoppingList=addToShoppingList)


