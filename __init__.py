from flask import Flask, url_for, request, render_template, Blueprint, redirect
from flask.ext.login import login_required, current_user
from flask import Flask, url_for, request
from flask import render_template
from flask.ext.login import LoginManager
from flask.ext.mongoengine import MongoEngine
from config import app, db
from authentication import login_manager
from flask.ext.login import current_user
from DinnerTrackingGuide.models import User

def register_blueprints(app):
	from DinnerTrackingGuide.views import users
	app.register_blueprint(users)

register_blueprints(app)

# SHOPPING_LIST
@app.route('/shopping/')
def shopping():
	shoppingList = []
	if current_user.is_authenticated():
			currUser = User.objects.get(id_token=current_user.get_id())
			shoppingList = currUser.shoppingList.split('\n')
			print "!!! shopping list contains %s" % currUser.username
			return render_template('shopping_list.html', items=shoppingList)
	else:
		return redirect(url_for('users.login'))

@app.context_processor
def utility_processor():
	def addToShoppingList(ingredients):
		print "shopping list was called with %s" % ingredients
		if current_user.is_authenticated():
			currUser = User.objects.get(id_token=current_user.get_id())
			foo = '\n'
			if currUser.shoppingList is not None:
				foo += currUser.shoppingList
			currUser.shoppingList = ingredients + foo;
			currUser.save()
			print "!!! userList contains %s" % currUser.shoppingList
			return '/shopping/'
		else:
			return redirect(url_for('users.login'))
	return dict(addToShoppingList=addToShoppingList)