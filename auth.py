from functools import wraps
from flask import request, Response

def check_auth(username, password):
	"""
	This is called to check the validity of a combination is valid"""
	return username == 'admin' and password == 'secret'

def authenticate():
	"""sends a 401 response that enables basic auth"""
	return Response(
		'could not verify who you are.\n'
		'You must log in with proper credentials', 401, 
		{'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		auth = request.authorization
		if not auth or check_auth(auth.username, auth.password):
			return authenticate()
		return f(*args, **kwargs)
	return decorated