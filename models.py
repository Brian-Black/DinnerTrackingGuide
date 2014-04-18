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
	title = db.StringField(max_length=255, required=True)
	slug = db.StringField(max_length=255, required=True)
	author = db.StringField(max_length=255, required=True)
	id = db.StringField(required=True)
	username = db.StringField(required=True)
	recipes = db.ListField(db.EmbeddedDocumentField('Recipe'))
	
	def get_absolute_url(self):
		return url_for('my_recipes', kwargs={"slug": self.slug})
	
	def __unicode__(self):
		return self.title
	
	meta = {
		'allow_inheritance': True,
		'indexes': ['-created_at', 'slug'],
		'ordering': ['-created_at']
	}
    
    	def __init__(self):
		self.authenticated = None
		self.user_id = 'guest'
	
	def set_authenticated(self, auth):
		self.authenticated = auth
	
	def is_authenticated(self):
		#print 'is_authenticated called on user with id %s' % self.user_id
		#if(self.authenticated):
			#print 'True'
		#else:
			#print 'False'
		return self.authenticated

	def is_active(self):
		return True;

	def is_anonymous(self):
		return None
	
	def set_id(self, id):
		self.user_id = id

	def get_id(self):
		#print 'get_id called - returning %s' % self.user_id
		return self.user_id


        