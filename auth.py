'''
This is the authentication module for checking logins, rendering things, etc.
'''

import hashlib
import web

SALT = 'sleepfuriously'
session = web.config._session

def hash_password(s):
	'''Hash a password string with salt
	'''

	return hashlib.sha1(str(SALT + password).encode('utf-8')).hexdigest()

def logged():
	'''Is the user logged in?
	'''
	return session.login == 1

def create_render(privilege):
	'''Returns the rendered template, given the privilege level of the user.
	By default, the privilege for a logged-in user is 1, and 0 for a non-logged-in user.
	'''

	if logged():
		if privilege == 0:
			render = web.template.render('templates/common')
		else:
			render = web.template.render('templates/user')
	else:
		render = web.template.render('templates/common')
	return render

def login_required(route):
	'''
	This route requires the user to be logged in.
	'''

	def required(*args):
		if logged():
			return route(*args)
		else:
			return web.template.render('templates').login_required()

	return required