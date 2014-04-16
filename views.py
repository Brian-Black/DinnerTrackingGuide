from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
from DinnerTrackingGuide.models import Recipe, Comment
from flask.ext.mongoengine.wtf import model_form

recipes = Blueprint('recipes', __name__, template_folder='templates')

class HomeView(MethodView):

	def get(self):
		recipes = Recipe.objects.all()
		return render_template('testLanding.html', recipes=recipes)

class RecipeView(MethodView):

	form = model_form(Comment, exclude=('created_at'))

	def get_context(self, slug=None):

		recipe = Recipe.objects.get_or_404(slug=slug)
		form = self.form(request.form)
		
		context = {
			"recipe": recipe,
			"form": form
		}
		return context

	def get(self, slug):
		context = self.get_context(slug)
		return render_template('testDetail.html', **context)

	def post(self, slug):
		context = self.get_context(slug)
		form = context.get('form')

		if form.validate():
			comment = Comment()
			form.populate_obj(comment)
			
			recipe = context.get('recipe')
			recipe.comments.append(comment)
			recipe.save()

			return redirect(url_for('recipes.detail', slug=slug))
		return render_template('testDetail.html', **context)

class AddRecipeView(MethodView):

	def get_context(self, slug=None):
	
		form_cls = model_form(Recipe, exclude=('created_at', 'comments', 'totalRatings', 'NumberOfRatings'))

		if slug:
			recipe = Recipe.objects.get_or_404(slug=slug)
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

			return redirect(url_for('recipes.home', slug=slug))
		return render_template('testDetail.html', **context)


recipes.add_url_rule('/', view_func=HomeView.as_view('home'))
recipes.add_url_rule('/<slug>/', view_func=RecipeView.as_view('detail'))
recipes.add_url_rule('/create/', defaults={'slug': None}, view_func=AddRecipeView.as_view('create'))
recipes.add_url_rule('/edit/<slug>/', view_func=RecipeView.as_view('edit'))