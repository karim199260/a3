import re, math, collections, itertools, os
import nltk
from nltk.classify import util, NaiveBayesClassifier
import nltk.metrics
from nltk.metrics import BigramAssocMeasures
from nltk.probability import FreqDist, ConditionalFreqDist
import logging

POLARITY_DATA_DIR = os.path.join('sentiment/polarityData', 'rt-polaritydata')
RT_POLARITY_POS_FILE = os.path.join(POLARITY_DATA_DIR, 'rt-polarity-pos.txt')
RT_POLARITY_NEG_FILE = os.path.join(POLARITY_DATA_DIR, 'rt-polarity-neg.txt')


#this function takes a feature selection mechanism and returns its performance in a variety of metrics
def evaluate_features(feature_select, best_words):
    posFeatures = []
    negFeatures = []
    #http://stackoverflow.com/questions/367155/splitting-a-string-into-words-and-punctuation
    #breaks up the sentences into lists of individual words (as selected by the input mechanism) and appends 'pos' or 'neg' after each list
    with open(RT_POLARITY_POS_FILE, 'r') as posSentences:
        for i in posSentences:
            posWords = re.findall(r"[\w']+|[.,!?;]", i.rstrip())
            posWords = [feature_select(posWords, best_words), 'pos']
            posFeatures.append(posWords)
    with open(RT_POLARITY_NEG_FILE, 'r') as negSentences:
        for i in negSentences:
            negWords = re.findall(r"[\w']+|[.,!?;]", i.rstrip())
            negWords = [feature_select(negWords, best_words), 'neg']
            negFeatures.append(negWords)

    
    #selects 3/4 of the features to be used for training and 1/4 to be used for testing
    posCutoff = int(math.floor(len(posFeatures)*3/4))
    negCutoff = int(math.floor(len(negFeatures)*3/4))
    trainFeatures = posFeatures[:posCutoff] + negFeatures[:negCutoff]
    testFeatures = posFeatures[posCutoff:] + negFeatures[negCutoff:]

    #trains a Naive Bayes Classifier
    classifier = NaiveBayesClassifier.train(trainFeatures)  

    #initiates referenceSets and testSets
    referenceSets = collections.defaultdict(set)
    testSets = collections.defaultdict(set) 

    #puts correctly labeled sentences in referenceSets and the predictively labeled version in testsets
    for i, (features, label) in enumerate(testFeatures):
        referenceSets[label].add(i)
        predicted = classifier.classify(features)
        testSets[predicted].add(i)  

    #prints metrics to show how well the feature selection did
    print 'train on %d instances, test on %d instances' % (len(trainFeatures), len(testFeatures))
    print 'accuracy:', nltk.classify.util.accuracy(classifier, testFeatures)
    classifier.show_most_informative_features(10)


#creates a feature selection mechanism that uses all words
def make_full_dict(words):
    return dict([(word, True) for word in words])

# scores words based on chi-squared test to show information gain 
# (http://streamhacker.com/2010/06/16/text-classification-sentiment-analysis-eliminate-low-information-features/)
def create_word_scores(sentences):
    # logging.info(sentences)
    words = list(itertools.chain(*sentences))
    # logging.info(words)

    #build frequency distibution of all words and then frequency distributions of words within positive and negative labels
    word_fd = FreqDist()
    cond_word_fd = ConditionalFreqDist()
    for word in words:
        word_fd.inc(word.lower())
        cond_word_fd['pos'].inc(word.lower())
        cond_word_fd['neg'].inc(word.lower())
        
    #finds the number of positive and negative words, as well as the total number of words
    pos_word_count = cond_word_fd['pos'].N()
    neg_word_count = cond_word_fd['neg'].N()
    total_word_count = pos_word_count + neg_word_count

    #builds dictionary of word scores based on chi-squared test
    word_scores = {}
    for word, freq in word_fd.iteritems():
        pos_score = BigramAssocMeasures.chi_sq(cond_word_fd['pos'][word], (freq, pos_word_count), total_word_count)
        neg_score = BigramAssocMeasures.chi_sq(cond_word_fd['neg'][word], (freq, neg_word_count), total_word_count)
        word_scores[word] = pos_score + neg_score

    return word_scores


#finds the best 'number' words based on word scores
def find_best_words(word_scores, number):
    best_vals = sorted(word_scores.iteritems(), key=lambda (w, s): s, reverse=True)[:number]
    best_words = set([w for w, s in best_vals])
    return best_words

#creates feature selection mechanism that only uses best words
def best_word_features(words, best_words):
    return dict([(word, True) for word in words if word in best_words])


def get_sentiment(sentences):
    word_scores = create_word_scores(sentences)
    logging.info('WORD SCORES:')
    # logging.info(word_scores)
    num = 15000
    print 'evaluating best %d word features' % (num)
    best_words = find_best_words(word_scores, num)
    logging.info('BEST WORDS:')
    # logging.info(best_words)
    evaluate_features(feature_select=best_word_features, best_words=best_words)
