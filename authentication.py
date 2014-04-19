from flask import Blueprint, render_template, redirect, url_for, request, flash, session, Flask
from flask_oauth import OAuth
from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required

from mongoengine import *

from models import User
from config import *

#from config import *
#from models.user import *

connect('dinnerplanner')

# Login Setup
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
    print "login_user called"
    users = User.objects.all()
    for user in users:
        print "id = %s" % user.id_token
        if(user.id_token == userid):
            return user
    return None


# OAuth Setup
oauth = OAuth()
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
    if current_user.is_authenticated():
        next_url = request.args.get('next') or url_for('index')
        return redirect(next_url)
    next_url=request.args.get('next') or request.referrer or None
    callback='http://dinnerplanner.example.com:5000/auth/oauth'
    return google.authorize(callback=callback)
    #return google.authorize(callback=url_for('oatherized', next=next_url))

@auth.route('/oauth')
@google.authorized_handler
def authorized(resp):
    next_url = request.args.get('next') or url_for('index')
    if resp is None:
        flash(u'You denied the request to sign in.')
        return redirect(next_url)
    
    #user = User.get(resp['screen_name'])
    #if user is None:
        #user = User(resp['screen_name'], resp['oauth_token'], resp['oauth_token_secret'])
        #db.session.add(user)
        #db.session.commit()
        #login_user(user)
        #resp = twitter.get('/1.1/users/show.json?screen_name=' + user.username)
        #print resp.status
        #print resp.data
        #if resp.status == 200:
        #    print resp.data['name']
        #    user.name = resp.data['name']
        #    db.session.add(user)
        #    db.session.commit()
        #else:
        #login_user(user)
		
#    theUserOfTheMoment = User()
#    theUserOfTheMoment.set_id(resp['id_token'])
#    theUserOfTheMoment.set_authenticated(True)
#    login_user(theUserOfTheMoment)
    
    #user = User(username = 'bob', email = 'example@example.com', slug=resp['id_token']).save()
    user = User()
    user.username = 'bob'
    user.email = 'person@example.com'
    user.slug = 'bob'
    user.id_token = resp['id_token']
    user.authenticated = 'True'
    user.save()
    login_user(user)
    
    print "CHECKING to see if user was saved"
    users = User.objects.all()
    for user in users:
        print "id = %s" % user.id_token

    flash(u'You logged in sucessfully.')
    
    if not current_user.is_authenticated():
        print "current user is not authenticated"
    else:
        print "current user IS authenticated"

    return redirect(next_url)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/')

@google.tokengetter
def get_google_token():
    if current_user.is_authenticated():
        return (current_user.token, current_user.secret)
    else:
        return None
        

