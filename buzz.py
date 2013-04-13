import re
#from nltk.corpus import stopwords

# Assignment Text:

# 4. Buzz Extraction
# Write a buzz extraction module in which you extract the top 10 popular buzzes. You 
# could at the minimum determine the frequency of "significant" words and use that count 
# to determine the top buzzes. You are welcome use more sophisticated approaches.
 
# For example, if the category is "sports" - you might find "baseball", "basketball", 
# "football" and "miami heats" as high frequency words in tweets. 


def get_significant_words(tweet_body):
	""" gets significant terms from a tweet by 1) tokenizing the tweet and 2) eliminating stopwords (such as 'is', 'as', or 'and')
	:param tweet_body: a string containing the content of one tweet
	:returns: an array of words
	"""

	# #remove punctuation and split into seperate words
	# words = re.findall(r'\w+', tweet_body.lower(), flags = re.UNICODE | re.LOCALE) 

	# significant_words = filter(lambda x: x not in stopwords.words('english'), words)

	# dummy return code, so this method can be called before it is fully implemented
	return ['term1', 'term2', 'term3']