import web
import hashlib

web.config.debug = False

# Routing
urls = (
	'/login', 'Login',
	'/reset', 'Reset',
	'/signup', 'Signup',
)

from db import db

app = web.application(urls, globals())

# Session configuration
if web.config.get('_session') is None:
	store = web.session.DiskStore('sessions')
	session = web.session.Session(app, store, initializer={'login': 0, 'privilege': 0, 'id': ''})
	web.config._session = session
else:
	session = web.config._session

from signup import Signup
from reset import Reset
from login import Login

if __name__ == '__main__':
	app.run()
