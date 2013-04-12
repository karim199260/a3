import cgi
import datetime
import urllib
import webapp2
import jinja2
import os

import location

from google.appengine.ext import db
from google.appengine.api import users

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


class MainPage(webapp2.RequestHandler):
	def get(self):
		gc_name=self.request.get('gc_name')
		if (gc_name == None):
			gc_address=""
		else:
			gc_address=location.search(gc_name)

		template_values = {
			'gc_name': gc_name,
			'gc_address': gc_address
		}

		template = jinja_environment.get_template('index.html')
		self.response.out.write(template.render(template_values))

class GetCoordinates(webapp2.RequestHandler):
	def post(self):
		gc_name = self.request.get('gc_name')
		self.redirect('/?' + urllib.urlencode({'gc_name': gc_name}))

mappings = [
	('/', MainPage),
	('/get_coordinates', GetCoordinates)
]
app = webapp2.WSGIApplication(mappings, debug=True)