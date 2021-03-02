'''
This is the module for resetting the user's session (after they press logout).
'''

from auth import create_render, session

class Reset:
	def GET(self):
		session.login = 0
		session.kill()
		render = create_render(session.privilege)
		return render.logout()