import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask.ext.script import Manager, Server
from DinnerTrackingGuide import app

from authentication import auth
app.register_blueprint(auth, url_prefix="/auth")

manager = Manager(app)

manager.add_command("runserver", Server(
    use_debugger = True,
    use_reloader = True,
	host = 'dinnerplanner.example.com',
	port = '5000')
)
					#host = '0.0.0.0')

if __name__ == "__main__":
    manager.run()
