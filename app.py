import web
import hashlib
from decouple import config

web.config.debug = False

urls = (
	'/login', 'Login',
	'/reset', 'Reset',
	'/signup', 'Signup',
)

# Salt for hashing passwords
SALT = 'colorlessgreenideas'

DB_USER = config('DBUSER')
DB_PASS = config('DBPASS')
db = web.database(dbn='mysql', db='db', user=DB_USER, pw=DB_PASS)

logged = lambda: session.login == 1

def create_render(privilege):
	if logged():
		if privilege == 0:
			render = web.template.render('templates/common')
		else:
			render = web.template.render('templates/user')
	else:
		render = web.template.render('templates/common')
	return render

class Login:
	def GET(self):
		if logged():
			render = create_render(session.privilege)
			return '%s' % render.login()
		else:
			render = create_render(session.privilege)
			return '%s' % render.login()
	def POST(self):
		username, password = web.input().username, web.input().password
		identity = db.select('users', where='user=$username', vars=locals())[0]
		try:
			if hashlib.sha1(str(SALT + password).encode('utf-8')).hexdigest() == identity['pass']:
				session.login = 1
				session.privilege = identity['privilege']
				render = create_render(session.privilege)
				return render.login_ok()
			else:
				session.login = 0
				session.privilege = 0
				render = create_render(session.privilege)
				return render.login_error()
		except:
			session.login = 0
			session.privilege = 0
			render = create_render(session.privilege)
			return render.login_error()

class Reset:
	def GET(self):
		session.login = 0
		session.kill()
		render = create_render(session.privilege)
		return render.logout()

class Signup:
	def GET(self):
		if logged():
			render = create_render(session.privilege)
			return '%s' % render.signup()
		else:
			render = create_render(session.privilege)
			return '%s' % render.signup()
	def POST(self):
		form = web.input()
		email, username, password = form.email, form.username, form.password

		hashed = hashlib.sha1(str(SALT + password).encode('utf-8')).hexdigest()
		args = {
			'user': username,
			'pass': hashed,
			'email': email
		}
		db.insert('users', **args)

		identity = db.select('users', where='user=$username', vars=locals())[0]
		session.login = 1
		session.privilege = identity['privilege']
		
		render = create_render(session.privilege)
		return render.login_ok()

app = web.application(urls, globals())
store = web.session.DiskStore('sessions')
session = web.session.Session(app, store, initializer={'login': 0, 'privilege': 0})

if __name__ == '__main__':
	app.run()

