'''
This is the module for signing up new users in the database.
'''

from auth import logged, hash_password, create_render, session, login_required

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

		hashed = hash_password(password)
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