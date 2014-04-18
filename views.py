from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
from DinnerTrackingGuide.models import Users, Recipe, Comment
from flask.ext.mongoengine.wtf import model_form
from DinnerTrackingGuide.auth import requires_auth
from flask.ext.login import current_user

users = Blueprint('users', __name__, template_folder='templates')

class HomeView(MethodView):
	def get(self):
		return render_template('base.html')

class UserView(MethodView):

	def get_context(self, slug=None):
		#user = Users.objects.get_or_404(slug=slug)
		form = model_form(Users, exclude=('created_at'))

		context = {
		#	"user": user,
			"form": form
		}

		return context

	def get(self, slug):
		#form = model_form(Recipe, exclude=('created_at', 'comments'))
		context = self.get_context(slug)

		if current_user.is_authenticated():
			user = self.get_context(slug)
			return render_template('testLanding.html', user=user)
		else:
			return render_template('login.html', **context)

class RecipeView(MethodView):

	form = model_form(Comment, exclude=('created_at'))

	def get_context(self, slug=None):

		recipe = Recipe.objects(slug=slug)
		form = self.form(request.form)
		
		context = {
			"recipe": recipe,
			"form": form
		}
		return context

	def get(self, slug):
		context = self.get_context(slug)
		return render_template('testDetail.html', **context)

	def post(self, slug, author):
		context = self.get_context(slug)
		form = context.get('form')

		if form.validate():
			comment = Comment()
			form.populate_obj(comment)
			
			recipe = context.get('recipe')
			recipe.comments.append(comment)
			recipe.save()

			return redirect(url_for('users.detail', slug=slug, author=author))
		return render_template('testDetail.html', **context)

class AddRecipeView(MethodView):

	def get_context(self, slug=None):
	
		form_cls = model_form(Recipe, exclude=('created_at', 'slug', 'comments', 'totalRatings', 'NumberOfRatings'))

		if slug:
			recipe = Users.recipes.get_or_404(slug=slug)
			if request.method == 'POST':
				form = form_cls(request.form, initial=recipe._data)
			else:
				form = form_cls(obj=recipe)
		else:
			recipe = Recipe()
			form = form_cls(request.form)

		context = {
			"recipe": recipe,
			"form": form,
			"create": slug is None
		}
		return context

	def get(self, slug):
		context = self.get_context(slug)
		return render_template('addRecipe.html', **context)

	def post(self, slug):
		context = self.get_context(slug)
		form = context.get('form')

		if form.validate():
			recipe = context.get('recipe')
			form.populate_obj(recipe)
			recipe.save()

			return redirect(url_for('users.home', slug=slug))
		return render_template('testDetail.html', **context)


users.add_url_rule('/', view_func=HomeView.as_view('home'))
users.add_url_rule('/login/', defaults={'slug': None}, view_func=UserView.as_view('login'))
users.add_url_rule('/<slug>/', view_func=RecipeView.as_view('detail'))
users.add_url_rule('/create/', defaults={'slug': None}, view_func=AddRecipeView.as_view('create'))
users.add_url_rule('/edit/<slug>/', view_func=RecipeView.as_view('edit'))