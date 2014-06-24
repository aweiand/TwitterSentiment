# # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#  Twitter Sentiment Classifier
#
#   - Augusto Weiand
#     guto.weiand@gmail.com
#     June 10, 2014
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # #

import csv
import nltk
from nltk.classify.naivebayes import NaiveBayesClassifier
from nltk.corpus import stopwords
from sklearn import cross_validation

def getUniqueItems(iterable):
    result = []
    for item in iterable:
        item_clean = item.replace(".","").replace(",", "").replace("!","").lower()
        if item_clean not in result:
            result.append(item_clean)
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

def print_menu():
    print ("Menu:")
    print ("Tweets positivos: p pos")
    print ("Tweets negativos: p neg")
    print ("Mostrar o menu: p menu")
    print ("Sair: q")
    print ("--------\n")

def print_status(tipo):
    qtd = int(raw_input('\nDigite quantos resultados voce quer ver: '))
    print("\n--------\n Top %d - Tweets %s:" % (qtd, tipo.upper()))

    for tweet in in_tweets:
        if qtd == 0:
            break

        classified = classify_tweet(tweet[0])
        if classified == tipo and tweet[1] == tipo:
            print("%s" % (tweet[0]))
            qtd -= 1

    print("--------\n")

# read in training tweets
print("Lendo tweets de treino...\n")
in_tweets       = read_tweets('./GetTwitterCorpus/full-corpus-2col-2class.csv')
number_cross    = round(len(in_tweets) * 0.10)

# filter away words form the training data
print("Removendo palavras com menos de 3 letras dos tweets de treino...\n")
tweets      = []
portStem    = nltk.stem.porter.PorterStemmer()
stop        = stopwords.words('english')

for (words, sentiment) in in_tweets:
    words_filtered = []
    for e in words.split():
        if e not in stop:
            words_filtered.append(portStem.stem(e))

    tweets.append((words_filtered, sentiment))


# extract the word features out from the training data
word_features = get_word_features(get_words_in_tweets(tweets))

# get the training set and train the Naive Bayes Classifier
print("Aplicando o treino com o Naive Bayes Classifier (by NLTK)...\n")
training_set = nltk.classify.util.apply_features(extract_features, tweets)
cv = cross_validation.KFold(len(training_set), n_folds=number_cross, indices=True, shuffle=False, random_state=None, k=None)

totalaccuracy = 0
test = { 'positive': 0, 'negative': 0, 'totpos': 0, 'totneg': 0 }
for tweet, testcv in cv:
    classifier  = NaiveBayesClassifier.train(training_set[tweet[0]:tweet[len(tweet)-1]])
    accuracy    = nltk.classify.util.accuracy(classifier, training_set[testcv[0]:testcv[len(testcv)-1]])

    totalaccuracy += accuracy

    classified     = classify_tweet(in_tweets[testcv[0]][0])
    # print 'accuracy:', accuracy
    # print ("Tweet: ... : Pre-class: %s || Classificado como: %s" % (in_tweets[testcv[0]][1], classified))
    if classified == 'positive':
        test['positive'] += 1
    else:
        test['negative'] += 1

    if in_tweets[testcv[0]][1] == 'positive':
        test['totpos'] += 1
    else:
        test['totneg'] += 1

print ("\n--------")
print ('Cross Validation with: %d folds (%d%%) of %d' % (number_cross, (number_cross * 100) / len(tweet), len(tweet)))
print ('Total accuracy on CV: %f' % (totalaccuracy / number_cross))
print ('Positives: %d of %d' % (test['positive'], test['totpos']))
print ('Negatives: %d of %d' % (test['negative'], test['totneg']))
print ("\n--------")

print_menu()
print ("\n--------")
inpt = raw_input( '\nDigite outro texto para classificar ou "q" para sair: ' )
while inpt != 'q':
    if inpt == 'p menu':
        print_menu()
    if (inpt == 'p neg'):
        print_status('negative')
    elif (inpt == 'p pos'):
        print_status('positive')
    else:
        print("--------\n")
        classified = classify_tweet(inpt.lower())
        print("O texto: %s foi classificado como %s " % (inpt, classified))
        print("--------\n")

    inpt = raw_input( '\nDigite outro texto para classificar ou "q" para sair: ' )
