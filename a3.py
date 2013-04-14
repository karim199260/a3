import datetime
import logging
import webapp2
import jinja2
import os

from google.appengine.ext import db
from google.appengine.api import users
from sentiment.text_processing import get_sentiment, get_mean_sentiment

import buzz
import google_geocode
import twitter

NUM_BUZZES = 10
MAX_TWEETS_PER_BUZZ = 99

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

def get_tweets(search_term, location, location_name):
	'''Gets the tweets for a given location. It tries the Google Datastore first; that failing,
	it grabs new tweets from Twitter.
	:param location: the google geocode location coordinates
	:param location_name: the named location
	:param search_term: twitter is queried with this'''
	
	# First, check whether tweets for this search term and location already exist in the db.
	q = twitter.Tweet.all()
	q.filter("location_name =", location_name.lower())
	q.filter("search_term =", search_term)
	tweet_records = q.run(limit=10, read_policy=db.STRONG_CONSISTENCY)
	tweet_records = list(tweet_records)

	if len(tweet_records) > 0:
		logging.info('using cached tweets')

	# If they don't, fetch the tweets and put them in the db
	if len(tweet_records) == 0:
		logging.debug('no cached tweets; fetching new ones')
		tweet_records = []
		tweets = twitter.get_tweets(search_term, location)

		for tweet in tweets:
			# e.g. Sat, 13 Apr 2013 21:50:12 +0000
			dt = datetime.datetime.strptime(tweet['created_at'],'%a, %d %b %Y %H:%M:%S +0000')

			# Get the tweet's sentiment
			sentiment = get_sentiment(tweet['text'])
			
			record = twitter.Tweet(	text=tweet['text'],
									from_user=tweet['from_user'],
									profile_image_url=tweet['profile_image_url'],
									created_at=dt,
									location_name=location_name.lower(),
									search_term=search_term,
									pos=sentiment['probability']['pos'],
									neg=sentiment['probability']['neg'],
									neutral=sentiment['probability']['neutral'],
									label=sentiment['label']
									)
			record.put()  # persist to the db
			tweet_records.append(record)  # collect for immediate return

	return tweet_records

class MainPage(webapp2.RequestHandler):
	def post(self):

		def redirect_to_index(error=None):
			if error:
				context['error'] = error
			template = jinja_environment.get_template('index.html')
			self.response.out.write(template.render(context))

		location_name = self.request.get('location_name').strip()
		search_term = self.request.get('search_term').strip()

		context = {
			'location_name': location_name,
			'search_term': search_term
		}

		# If search terms entered, perform search
		if location_name and search_term:
			location = google_geocode.search(location_name)

			# User entered non-location
			if not location:
				redirect_to_index(error='Please enter a valid location.')
				return

			context['location'] = location
			tweets = get_tweets(search_term, location, location_name)

			if len(tweets) == 0:
				redirect_to_index(error=u"We couldn't find any tweets. Please try again.")
				return

			words = []
			for t in tweets:
				words.extend(buzz.get_significant_words(t.text))
			buzzwords = buzz.get_most_common_words(words_list=words, num_words=NUM_BUZZES)
			logging.info(buzzwords)

			buzzes = []
			for i in range(len(buzzwords)):
				buzzword = buzzwords[i]
				filtered_tweets = [t for t in tweets if buzzword.lower() in t.text.lower()][:MAX_TWEETS_PER_BUZZ]
				label, prob, hot = get_mean_sentiment(filtered_tweets)

				# For CSS styling
				info_class = dict(positive='success', negative='error', neutral='info')[label]

				b = dict(
					rank=i+1,
					buzzword=buzzword,
					tweets=filtered_tweets,
					sentiment_label=label,
					sentiment_prob=prob,
					sentiment_hot=hot,
					info_class=info_class,
					)
				buzzes.append(b)

			context['buzzes'] = buzzes

		else:
			redirect_to_index(error='Please submit both the location name and the search term.')
			return

		redirect_to_index()

	def get(self):
		template = jinja_environment.get_template('index.html')
		self.response.out.write(template.render())


mappings = [
	('/', MainPage),
]
app = webapp2.WSGIApplication(mappings, debug=True)