from TextProcessing import TextProcessing

client = TextProcessing("xslgc26CVzxMaUUF1QhmQASVgjGdY7Tj")

def get_sentiment(text):
	response = client.sentiment(text, language='english')
	return vars(response)['body']

if __name__ == '__main__':
	get_sentiment(text='I am very happy.')
	get_sentiment(text='I am very sad.')