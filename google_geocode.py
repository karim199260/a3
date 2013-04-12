import urllib
import json

from google.appengine.api import urlfetch

def search(search_terms):
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
		item = json.loads(result.content)['results']
		if (len(item) > 0):
			gps_coordinates = item[0]['geometry']['location']
			address = item[0]['formatted_address']
			return gps_coordinates
		else:
			return None