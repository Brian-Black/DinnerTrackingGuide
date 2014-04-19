from flask import Blueprint, render_template, redirect, url_for, request, flash, session, Flask
from flask_oauth import OAuth
from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required

from mongoengine import connect
from mongoengine.connection import _get_db

from mongoengine import *

from models import User
from config import *

#from config import *
#from models.user import *

# Login Setup
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
	users = User.objects.all()
	for user in users:
		if(user.id_token == userid):
			return user
	return None


# OAuth Setup
oauth = OAuth()
'''
google = oauth.remote_app('google',
                          base_url='https://www.google.com/accounts/',
                          authorize_url='https://accounts.google.com/o/oauth2/auth',
                          request_token_url=None,
                          request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.email',
						  'response_type': 'code'},
                          access_token_url='https://accounts.google.com/o/oauth2/token',
                          access_token_method='POST',
                          access_token_params={'grant_type': 'authorization_code'},
                          consumer_key=GOOGLE_CLIENT_ID,
                          consumer_secret=GOOGLE_CLIENT_SECRET)
'''						  

google = oauth.remote_app('google',
                          base_url='https://www.google.com/accounts/',
                          authorize_url='https://accounts.google.com/o/oauth2/auth',
                          request_token_url=None,
                          request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.email',
						  'response_type': 'code'},
                          access_token_url='https://accounts.google.com/o/oauth2/token',
                          access_token_method='POST',
                          access_token_params={'grant_type': 'authorization_code'},
                          consumer_key=GOOGLE_CLIENT_ID,
                          consumer_secret=GOOGLE_CLIENT_SECRET)

auth = Blueprint('auth', __name__)

# Google
@auth.route('/login')
def login():
	print 'login called'
	if current_user.is_authenticated():
		next_url = request.args.get('next') or url_for('users.home')
		return redirect(next_url)
	next_url=request.args.get('next') or request.referrer or None
	callback='http://dinnerplanner.example.com:5000/auth/oauth'
	return google.authorize(callback=callback)
	#return google.authorize(callback=url_for('oatherized', next=next_url))

@auth.route('/oauth')
@google.authorized_handler
def authorized(resp):
	print '*** authorized()'
	next_url = request.args.get('next') or url_for('users.home')
	if resp is None:
		flash(u'You denied the request to sign in.')
		return redirect(next_url)


	access_token = resp['access_token']
	session['access_token'] = access_token, ''
	
	access_token = session.get('access_token')
	if access_token is None:
		return redirect(url_for('login'))
	
	access_token = access_token[0]
	from urllib2 import Request, urlopen, URLError
	
	headers = {'Authorization': 'OAuth '+access_token}
	req = Request('https://www.googleapis.com/oauth2/v1/userinfo', None, headers)
	try:
		res = urlopen(req)
	except URLError, e:
		if e.code == 401:
			# Unauthorized - bad token
			session.pop('access_token', None)
			return redirect(url_for('login'))
	
	user_info = res.read()
	#print user_info
	
	id = user_info.index('id')
	start = user_info.index("\"", id+3)
	end = user_info.index("\"", id+6)
	id = user_info[start+1:end]
	
	email = user_info.index('email')
	start = user_info.index("\"", email+6)
	end = user_info.index("\"", email+9)
	email = user_info[start+1:end]
	
	name = user_info.index('name')
	start = user_info.index("\"", name+5)
	end = user_info.index("\"", name+8)
	name = user_info[start+1:end]
	
	user = None
	for registered_user in User.objects.all():
		if registered_user.id_token == id:
			user = registered_user
			break
			
	if user is None:
		user = User()
		user.username = name
		user.email = email
		user.slug = name
		user.id_token = id
		user.authenticated = 'True'
		user.save()
		
	login_user(user)
	flash(u'You logged in sucessfully.')
	return redirect(next_url)


@auth.route("/logout")
@login_required
def logout():
	current_user.authenticated = None
	logout_user()
	return redirect('/')

@google.tokengetter
def get_google_token():
	return session.get('access_token')
	

