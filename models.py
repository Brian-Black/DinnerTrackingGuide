import datetime
from flask import url_for
from DinnerTrackingGuide import db


class RecipeInDatabase(db.EmbeddedDocument):
	created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
	title = db.StringField(max_length=255, required=True)
	slug = db.StringField(max_length=255, required=True)
	author = db.StringField(max_length=255, required=True)
	instructions = db.StringField(required=True)
	ingredients = db.StringField(required=True)
	totalRatings = db.IntField()
	NumberOfRatings = db.IntField()
	comments = db.ListField(db.EmbeddedDocumentField('Comment'))

	def get_absolute_url(self):
		return url_for('recipe', kwargs={"slug": self.slug})

	def __unicode__(self):
		return self.title

	meta = {
		'allow_inheritance': True,
		'indexes': ['-created_at', 'slug'],
		'ordering': ['-created_at']
	}

class Comment(db.EmbeddedDocument):
	created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
	body = db.StringField(verbose_name="Comment", required=True)
	author = db.StringField(verbose_name="Name", max_length=255, required=True)


class User(db.Document):
	created_at = db.DateTimeField(default=datetime.datetime.now, required=True)
	username = db.StringField(required=True)
	email = db.StringField(required=True)
	slug = db.StringField(max_length=255, required=True)
	id_token = db.StringField(required=True)
	authenticated = db.StringField(required=True)
	
	def get_absolute_url(self):
		return url_for('my_recipes', kwargs={"slug": self.slug})
	
	def __unicode__(self):
		return self.title
	
	meta = {
		'allow_inheritance': True,
		'indexes': ['-created_at', 'slug'],
		'ordering': ['-created_at']
	}
	
	def is_authenticated(self):
		return self.authenticated == 'True'

	def is_active(self):
		return True;

	def is_anonymous(self):
		return None

	def get_id(self):
		return self.id_token





