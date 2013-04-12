import cgi
import datetime
import urllib
import webapp2
import jinja2
import os

import google_geocode
import twitter

from google.appengine.ext import db
from google.appengine.api import users

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


class MainPage(webapp2.RequestHandler):
	def get(self):
		location_name=self.request.get('location_name')
		search_term=self.request.get('search_term')

		template_values = {
			'location_name': location_name,
			'search_term': search_term,
			'location': '',
			'tweets': ''
		}

		# If search terms entered, perform search
		if (len(location_name) and len(search_term)):
			location = google_geocode.search(location_name)
			tweets = twitter.get_tweets(search_term, location)
			template_values['location'] = location;
			template_values['tweets'] = tweets;

		template = jinja_environment.get_template('index.html')
		self.response.out.write(template.render(template_values))

class GetCoordinates(webapp2.RequestHandler):
	def post(self):
		location_name = self.request.get('location_name')
		search_term = self.request.get('search_term')
		self.redirect('/?' + urllib.urlencode({'location_name': location_name, 'search_term': search_term}))

mappings = [
	('/', MainPage),
	('/get_coordinates', GetCoordinates)
]
app = webapp2.WSGIApplication(mappings, debug=True)