import cgi
import datetime
import logging
import time
import urllib
import webapp2
import jinja2
import os
import buzz

from google.appengine.ext import db
from google.appengine.api import users

import buzz
import google_geocode
import sentiment
import twitter

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

def get_tweets(search_term, location, location_name):
	'''Gets the tweets for a given location. It tries the Google Datastore first; that failing,
	it grabs new tweets from Twitter.
	:param location: the google geocode location coordinates
	:param location_name: the named location
	:param search_term: twitter is queried with this'''
	
	# First, check whether tweets for this search term and location already exist in the db.
	q = twitter.Tweet.all()
	q.filter("location_name =", location_name)
	q.filter("search_term =", search_term)
	tweet_records = q.run(limit=10, read_policy=db.STRONG_CONSISTENCY)
	tweet_records = list(tweet_records)

	if len(tweet_records) > 0:
		logging.info('using cached tweets')

	# If they don't, fetch the tweets and put them in the db
	if len(tweet_records) == 0:
		logging.critical('no cached tweets; fetching new ones')
		tweet_records = []
		tweets = twitter.get_tweets(search_term, location)

		for tweet in tweets:
			# e.g. Sat, 13 Apr 2013 21:50:12 +0000
			dt = datetime.datetime.strptime(tweet['created_at'],'%a, %d %b %Y %H:%M:%S +0000')
			record = twitter.Tweet(	text=tweet['text'],
									from_user=tweet['from_user'],
									profile_image_url=tweet['profile_image_url'],
									created_at=dt,
									location_name=location_name,
									search_term=search_term,
									)
			record.put()  # persist to the db
			tweet_records.append(record)  # collect for immediate return

	return tweet_records

class MainPage(webapp2.RequestHandler):
	def post(self):

		location_name = self.request.get('location_name')
		search_term = self.request.get('search_term')

		context = {
			'location_name': location_name,
			'search_term': search_term
		}

		# If search terms entered, perform search
		if location_name and search_term:
			location = google_geocode.search(location_name)
			tweets = get_tweets(search_term, location, location_name)
			context['location'] = location

			words = []
			for tweet in tweets:
				words.extend(buzz.get_significant_words(tweet.text))
			buzzwords = buzz.get_most_common_words(words_list=words, num_words=5)
			logging.info(buzzwords)

			buzzes = []
			for i in range(len(buzzwords)):
				buzzword = buzzwords[i]
				filtered_tweets = [t for t in tweets if buzzword in t.text]
				buzz_tweets = [ dict(from_user=t.from_user, text=t.text, profile_image_url=t.profile_image_url) 
								for t in filtered_tweets ]
				b = dict(
					rank=i+1,
					buzzword=buzzword,
					sentiment=sentiment.get_sentiment([t.text for t in filtered_tweets]),
					tweets=buzz_tweets,
					)
				buzzes.append(b)

			context['buzzes'] = buzzes

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