import cgi
import datetime
import urllib
import webapp2
import jinja2
import os

from google.appengine.api import users

import google_geocode
import twitter


jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))


cache = {}
def get_tweets(search_term, location):
	'''gets the tweets for a given location_name, via google geocode + twitter (tweets are memoized)
	:param location: the google geocode location coordinates
	:param search_term: twitter is queried with this'''
	# signature = (search_term, location['lat'], location['lng'])
	# if signature not in cache:
	# 	tweets = twitter.get_tweets(search_term, location)
	# 	cache[signature] = tweets
	# return cache[signature]
	return twitter.get_tweets(search_term, location)

class MainPage(webapp2.RequestHandler):
	def post(self):

		location_name = self.request.get('Location name')
		search_term = self.request.get('Search term')

		import logging; logging.info(self.request)

		context = {
			'location_name': location_name,
			'search_term': search_term,
			'location': '',
			'tweets': ''
		}

		# If search terms entered, perform search
		if location_name and search_term:
			location = google_geocode.search(location_name)
			tweets = get_tweets(search_term, location)
			context['location'] = location
			context['tweets'] = tweets
		else:
			context['error'] = 'Please submit both the location name and the search term.'

		template = jinja_environment.get_template('index.html')
		self.response.out.write(template.render(context))

	def get(self):
		template = jinja_environment.get_template('index.html')
		self.response.out.write(template.render())


mappings = [
	('/', MainPage),
]
app = webapp2.WSGIApplication(mappings, debug=True)