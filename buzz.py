import re
from collections import Counter

# Assignment Text:

# 4. Buzz Extraction
# Write a buzz extraction module in which you extract the top 10 popular buzzes. You 
# could at the minimum determine the frequency of "significant" words and use that count 
# to determine the top buzzes. You are welcome use more sophisticated approaches.
 
# For example, if the category is "sports" - you might find "baseball", "basketball", 
# "football" and "miami heats" as high frequency words in tweets. 


def get_most_common_words(words_list, num_words):
	""" gets n most common terms from a list words
	:param words_list: array of individual words
	:param num_words: number of top words to return
	:returns: an array of words
	"""

	# TODO: Collapse synonyms based on this API: http://wikisynonyms.ipeirotis.com/page/api

	most_common_words = [i[0] for i in Counter(words_list).most_common(num_words)]

	return most_common_words


def get_significant_words(tweet_body):
	""" gets significant terms from a tweet by 1) tokenizing the tweet and 2) eliminating stopwords (such as 'is', 'as', or 'and')
	:param tweet_body: a string containing the content of one tweet
	:returns: an array of words

	Example:
		The expression...
			buzz.get_significant_words("This is an example test tweet.")
		returns... 
			['example', 'test', 'tweet']
	"""

	# use list of stopwords as defined in the nltk (http://nltk.org/).  installed that separately since it is not
	# compatible with Google AppEngine, and exported the list of english stopwords, and copy-pasted here.  
	stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 
		'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 
		'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 
		'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 
		'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 
		'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 
		'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 
		'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 
		'should', 'now']

	#remove punctuation and split into individual words
	words = re.findall(r'\w+', tweet_body.lower(), flags = re.UNICODE | re.LOCALE) 

	significant_words = [i for i in words if (not i in stopwords)]

	# dummy return code, so this method can be called before it is fully implemented
	return significant_words