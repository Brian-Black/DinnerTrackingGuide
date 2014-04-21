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

# SHOPPING_LIST
shoppingList = []
@app.route('/shopping/')
def shopping():
	#return render_template('design_shopping_list.html', items=itmesForList)
	return render_template('shopping_list.html', items=shoppingList)

@app.context_processor
def utility_processor():
	def addToShoppingList(ingredients):
		print "shopping list was called with %s" % ingredients
		shoppingList.extend(ingredients)
		return '/shopping/'
	return dict(addToShoppingList=addToShoppingList)