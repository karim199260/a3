import urllib
import json

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
