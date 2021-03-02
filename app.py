import web
import hashlib
from decouple import config

web.config.debug = False

# Routing
urls = (
	'/login', 'Login',
	'/reset', 'Reset',
	'/signup', 'Signup',
)

# Database configuration
DB_USER = config('DBUSER')
DB_PASS = config('DBPASS')
db = web.database(dbn='mysql', db='db', user=DB_USER, pw=DB_PASS)

app = web.application(urls, globals())

# Session configuration
if web.config.get('_session') is None:
	store = web.session.DiskStore('sessions')
	session = web.session.Session(app, store, initializer={'login': 0, 'privilege': 0})
	web.config._session = session
else:
	session = web.config._session

from signup import Signup
from reset import Reset
from login import Login

if __name__ == '__main__':
	app.run()
