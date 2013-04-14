from TextProcessing import TextProcessing

client = TextProcessing("xslgc26CVzxMaUUF1QhmQASVgjGdY7Tj")

def sentiment(text):
	response = client.sentiment(text, language='english')
	return vars(response)['body']

def mean(l):
	return float(sum(l))/len(l) if len(l) > 0 else float('nan')

def mean_sentiment(tweets):
	pos = []
	neg = []
	neutral = []
	for tweet in tweets:
		pos.append(float(tweet.pos))
		neg.append(float(tweet.neg))
		neutral.append(float(tweet.neutral))
	pos = mean(pos)
	neg = mean(neg)
	neutral = mean(neutral)

	if neutral > 0.5:
		label = 'neutral'
		prob = neutral
	else:
		if pos > neg:
			label = 'positive'
			prob = pos
		else:
			label = 'negative'
			prob = neg

	hot = False
	if prob > 0.75:
		hot = True

	return label, prob, hot

if __name__ == '__main__':
	get_sentiment(text='I am very happy.')
	get_sentiment(text='I am very sad.')