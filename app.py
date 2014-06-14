import csv
import nltk
# from stemming.porter2 import stem
from nltk.classify.naivebayes import NaiveBayesClassifier
from nltk.corpus import stopwords

def getUniqueItems(iterable):
    result = []
    for item in iterable:
        if item not in result:
            result.append(item)
    return result

def get_words_in_tweets(tweets):
    all_words = []
    for (words, sentiment) in tweets:
        all_words.extend(words)
    return getUniqueItems(all_words)


def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features


def read_tweets(fname):
    tweets = []
    f = open(fname, 'r')
    reader = csv.reader( f, delimiter=',', quotechar='"' )

    for row in reader:
        tweets.append([row[1], row[0]])

    f.close()
    return tweets


def extract_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
      features['contains(%s)' % word] = (word in document_words)
    return features


def classify_tweet(tweet):
    return \
        classifier.classify(extract_features(nltk.word_tokenize(tweet)))


# read in training tweets
print("Lendo tweets de treino...\n")
in_tweets = read_tweets('./GetTwitterCorpus/full-corpus-2col.csv')

# filter away words that are less than 3 letters to form the training data
print("Removendo palavras com menos de 3 letras dos tweets de treino...\n")
tweets      = []
portStem    = nltk.stem.porter.PorterStemmer()
stop        = stopwords.words('english')

for (words, sentiment) in in_tweets:
    words_filtered = []
    for e in words.split():
        if len(e) >= 5:
            if e not in stop:
                words_filtered.append(stem(e))

    tweets.append((words_filtered, sentiment))


# extract the word features out from the training data
word_features = get_word_features(get_words_in_tweets(tweets))


# get the training set and train the Naive Bayes Classifier
print("Aplicando o treino com o Naive Bayes Classifier (by NLTK)...\n")
training_set = nltk.classify.util.apply_features(extract_features, tweets)
classifier = NaiveBayesClassifier.train(training_set)


# read in the test tweets and check accuracy
# to add your own test tweets, add them in the respective files
print("Realizando teste com tweets de teste.\n")
test_tweets = read_tweets('./GetTwitterCorpus/test-corpus.csv')
total = accuracy = len(test_tweets)

# i = 0
for tweet in test_tweets:
    # if i < 10:
    print ("Tweet: ... : Pre-class: %s || Classificado como: %s" % (tweet[1], classify_tweet(tweet[0])))
        # i += 1

    if classify_tweet(tweet[0]) != tweet[1]:
        accuracy -= 1

print('Total accuracy: %f (%d/%d).' % (((accuracy *100) / total), accuracy, len(test_tweets)))
