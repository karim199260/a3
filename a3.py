import cgi
import datetime
import urllib
import webapp2

from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.api import urlfetch

import jinja2
import os

jinja_environment = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class Greeting(db.Model):
  """Models an individual Guestbook entry with an author, content, and date."""
  author = db.StringProperty()
  content = db.StringProperty(multiline=True)
  date = db.DateTimeProperty(auto_now_add=True)


def guestbook_key(guestbook_name=None):
  """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
  return db.Key.from_path('Guestbook', guestbook_name or 'default_guestbook')


class MainPage(webapp2.RequestHandler):
	def get(self):
		gc_name=self.request.get('gc_name')
		if (gc_name == None):
			gc_address=""
		else:
			gc_address=geocoder_get_address(gc_name)

		# if users.get_current_user():
		#     url = users.create_logout_url(self.request.uri)
		#     url_linktext = 'Logout'
		# else:
		#     url = users.create_login_url(self.request.uri)
		#     url_linktext = 'Login'

		template_values = {
			'gc_name': gc_name,
			'gc_address': gc_address
		}

		template = jinja_environment.get_template('index.html')
		self.response.out.write(template.render(template_values))

class GetCoordinates(webapp2.RequestHandler):
  def post(self):
	# # We set the same parent key on the 'Greeting' to ensure each greeting is in
	# # the same entity group. Queries across the single entity group will be
	# # consistent. However, the write rate to a single entity group should
	# # be limited to ~1/second.
	gc_name = self.request.get('gc_name')
	# greeting = Greeting(parent=guestbook_key(guestbook_name))

	# if users.get_current_user():
	#   greeting.author = users.get_current_user().nickname()

	# greeting.content = self.request.get('content')
	# greeting.put()
	self.redirect('/?' + urllib.urlencode({'gc_name': gc_name}))

def geocoder_get_address(search_terms):
	""" Get address for search string """
	url = "https://maps.googleapis.com/maps/api/geocode/json"
	params = {
		"address": search_terms,
		"sensor": "false"
	}
	url_params = urllib.urlencode(params)
	result = urlfetch.fetch(url=url + '?' + url_params, 
							method=urlfetch.GET)
	if result.status_code == 200:
		return result.content


app = webapp2.WSGIApplication([('/', MainPage),
							   ('/get_coordinates', GetCoordinates)],
							  debug=True)