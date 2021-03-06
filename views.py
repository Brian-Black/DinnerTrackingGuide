from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
from DinnerTrackingGuide.models import User, RecipeInDatabase, Comment, Ingredient
from flask.ext.mongoengine.wtf import model_form
from DinnerTrackingGuide.auth import requires_auth
from flask.ext.login import current_user

users = Blueprint('users', __name__, template_folder='templates')

class HomeView(MethodView):
	def get(self):
		recipes = RecipeInDatabase.objects.all()
		return render_template('testLanding.html', recipes=recipes)

class UserView(MethodView):

	def get(self):
		
		if current_user.is_authenticated():
			currUser = User.objects.get(id_token=current_user.get_id())
			recipes = RecipeInDatabase.objects.filter(author=currUser.username)
			return render_template('myRecipes.html', myrecipes=recipes)
		else:
			return redirect('/auth/login')

class RecipeView(MethodView):

	form = model_form(Comment, exclude=('created_at'))

	def get_context(self, slug=None):

		recipe = RecipeInDatabase.objects.get_or_404(slug=slug)
		form = self.form(request.form)
		
		context = {
			"recipe": recipe,
			"form": form
		}
		return context

	def get(self, slug):
		context = self.get_context(slug)
		return render_template('recipe.html', **context)

	def post(self, slug):
		context = self.get_context(slug)
		form = context.get('form')

		if form.validate():
			comment = Comment()
			form.populate_obj(comment)
			
			recipe = context.get('recipe')
			recipe.comments.append(comment)
			recipe.save()

			return redirect(url_for('users.detail', slug=slug))
		return render_template('recipe.html', **context)

class AddRecipeView(MethodView):

	def get_context(self, slug=None):
	
		form_cls = model_form(RecipeInDatabase, exclude=('created_at', 'author', 'slug', 'comments'))
		#form2_cls = model_form(Ingredient)

		if slug:
			recipe = RecipeInDatabase.objects.get_or_404(slug=slug)
			#ingredient = recipe.ingredients
			if request.method == 'POST':
				form = form_cls(request.form, initial=recipe._data)
				#form2 = form2_cls(request.form, initial=ingredient._data)
			else:
				form = form_cls(obj=recipe)
				#form2 = form2_cls(obj=ingredient)
		else:
			recipe = RecipeInDatabase()
			#ingredient = Ingredient()
			form = form_cls(request.form)
			#form2 = form2_cls(request.form)

		context = {
			"recipe": recipe,
			#"ingredients": ingredient,
			"form": form,
			#"form2": form2,
			"create": slug is None
		}
		return context

	def get(self, slug):
		if(current_user.is_authenticated() == False):
			return redirect(url_for('users.login'))
		context = self.get_context(slug)
		return render_template('addRecipe.html', **context)

	def post(self, slug):
		if(current_user.is_authenticated() == False):
			return redirect(url_for('users.login'))

		context = self.get_context(slug)
		form = context.get('form')
		
		if form.validate():
			recipe = context.get('recipe')
			form.populate_obj(recipe)

			temp = User.objects.get(id_token=current_user.get_id())

			recipe.author = temp.username

			recipe.slug = recipe.title
			
			#ingredient = context.get('ingredients')
			#form2.populate_obj(ingredient)

			#recipe.ingredients.append(ingredient)
			recipe.save()

			return redirect(url_for('users.home', slug=slug))
		return render_template('recipe.html', **context)


users.add_url_rule('/', view_func=HomeView.as_view('home'))
users.add_url_rule('/login/', view_func=UserView.as_view('login'))
users.add_url_rule('/<slug>/', view_func=RecipeView.as_view('detail'))
users.add_url_rule('/myRecipes/', view_func=UserView.as_view('myRecipes'))
users.add_url_rule('/create/', defaults={'slug': None}, view_func=AddRecipeView.as_view('create'))
users.add_url_rule('/edit/<slug>/', view_func=AddRecipeView.as_view('edit'))
