from flask import Flask, jsonify
from DinnerTrackingGuide import db
from flask import abort

@app.route('/api/JSONapi.py/<string:recipeName>', methods = ['GET'])
def getRecipe():
	recipe = RecipeInDatabase.objects.get_or_404(title = recipeName)
	return jsonify( { 'Recipe': recipe } )


@app.route('/api/JSONapi.py/getAllRecipes', methods = ['GET'])
def getAllRecipes():
	recipes = RecipeInDatabase.objects.all()
	if len(recipes) == 0:
		abort(404)
	return jsonify( { 'Recipes': recipe } )


# http://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask