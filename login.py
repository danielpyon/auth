'''
This is the module for logging in a user.
'''

from auth import logged, hash_password, create_render, session

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
			if hash_password(password) == identity['pass']:
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