import urllib
import json

from google.appengine.ext import db
from google.appengine.api import urlfetch

# example search: http://search.twitter.com/search.json?q=interesting%20things&geocode=37.781157,-122.398720,25mi

def get_tweets(search_terms, geocode):
	""" Get 100 tweets matching search terms within 100 miles of the given geocode """
	url = 'http://search.twitter.com/search.json'
	params = {
		'q': search_terms,
		'geocode': str(geocode['lat']) + ',' + str(geocode['lng']) + ',100mi'
	}
	url_params = urllib.urlencode(params)
	result = urlfetch.fetch(url=url + '?' + url_params, 
							method=urlfetch.GET)

	if result.status_code == 200:
		items = json.loads(result.content)['results']
		return [r['text'] for r in items]



# class Employee(db.Model):
#   name = db.StringProperty(required=True)
#   role = db.StringProperty(required=True,
#                            choices=set(["executive", "manager", "producer"]))
#   hire_date = db.DateProperty()
#   new_hire_training_completed = db.BooleanProperty(indexed=False)
#   email = db.StringProperty()


# e = Employee(name="John",
#              role="manager",
#              email=users.get_current_user().email())
# e.hire_date = datetime.datetime.now().date()
# e.put()

class Tweet(db.Model):
	# id, text, from_user, from_user_name, Created_at, location
	id = db.IntegerProperty(required=True)