import csv
import twitter
import os, time
import sys, traceback
import re
import nltk
from string import punctuation
from nltk.corpus import sentiwordnet as swn
from textblob import TextBlob
from nltk.tokenize import TweetTokenizer

# credentials for connecting to twitter API.
api = twitter.Api(
    consumer_key='YnH8HtrVYhxmNSr4lLLpuI5MG',
    consumer_secret='gk5Je6TJT9Bt2M7lrxask8LYFv0s4l7U2mKEeVUg6I7tvgAFW5',
    access_token_key='1571106582-jSTOVFhv7o8AxXiceEv6Sx60njiuUPH0lr77oI8',
    access_token_secret='tE5wzDkRAijVNL5O6vfDQzHzyBWTGlEpvVN9Y6nhGACBz'
)

_stopwords = []


# Append the current directory path to the file required.
def getFullPath(fileName, isOutput=False):
    if (isOutput):
        dir = os.path.join(os.getcwd(), 'Data', 'FetchedData', 'FinalData', fileName)
    else:
        dir = os.path.join(os.getcwd(), 'Data', 'FetchedData', fileName)
    return dir


# Used for saving the corpus as file as soon as it is downloaded
def saveAfterDownload(trainingData, tweetDataFile):
    with open(tweetDataFile, 'w') as csvfile:
        fieldnames = ['Topic', 'Text']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # writer.writeheader();
        for _eachline in trainingData:
            try:
                writer.writerow({'Topic': _eachline.split(',')[0].split(':')[1].replace('"', ''),
                                 'Text': _eachline.split(',')[1].split(':')[1].replace('"', '')})
            except:
                continue


# Read and Write used to fetch the corpus file and extract only emotion and text in new file.
def readAndWriteCorpus(corpusFile, destFile):
    print(corpusFile)
    print(destFile)
    try:
        corpus = []
        with open(corpusFile, 'rU') as csvfile:
            lineReader = csv.reader(csvfile, delimiter=':')
            for row in lineReader:
                try:
                    corpus.append(row[1].split('\t')[1].strip('"') + ' : ' + row[2].split('\t')[0].strip('"') + ' , ' +
                                  row[2].split('\t')[1].strip('"') + ' : ' + '. '.join(row[3:]))
                except:
                    continue
        saveAfterDownload(corpus, destFile)
        print('Successfully written file ' + getFullPath(destFile))
    except:
        print '-' * 60
        traceback.print_exc(file=sys.stdout)
        print '-' * 60


# First processing of Tweets but the data needs to be sent as list parameter.
def processTweets(list_of_tweets):
    # The list of tweets is a list of dictionaries which should have the keys, "text" and "label"
    processedTweets = []
    # This list will be a list of tuples. Each tuple is a tweet which is a list of words and its label
    for tweet in list_of_tweets:
        processedTweets.append((_processTweet(tweet.split(',')[1]), tweet.split(',')[0]))
    return processedTweets


def customReplaceFunc(tweet):
    dicToReplace = {
        "it's": 'it is',
        "'ve": 'have',
        "'re": 'are',
        "ya": '',
        "u": 'you',
        "'m":'am',
        "'re":'are',
        "'d": 'would',
        "'s": 'is',
        "'m": 'am',
        "'t":'not',
        "n't":'not',

        #unncessary
        "amp":'',
        "yay":'',
        "ya":''
    }

    tknzr = TweetTokenizer()
    list_word = tknzr.tokenize(tweet)
    # print ['Original'] + list_word
    for index in range(0,len(list_word)):
        if (dicToReplace.has_key(list_word[index])):
            list_word[index] = dicToReplace.get(str(list_word[index]))
        elif "'" in list_word[index]:
            if (dicToReplace.has_key("'" + list_word[index].split("'")[1])):
                list_word[index] = list_word[index].split("'")[0] + ' ' + dicToReplace.get("'" + list_word[index].split("'")[1])
    tweet = ' '.join(list_word)
    # print(tweet)
    # time.sleep(5)
    return tweet


# Second processing of Tweets
def _processTweet(tweet):
    # 1. Convert to lower case
    tweet = tweet.lower()

    tweet = customReplaceFunc(tweet)

    # 2. Replace links with the word URL
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', tweet)
    # 3. Replace @username with "AT_USER"
    tweet = re.sub('@[^\s]+', 'AT_USER', tweet)
    # 4. Replace #word with word
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)

    tweet = nltk.word_tokenize(tweet)
    # This tokenizes the tweet into a list of words # Let's now return this list minus any stopwords
    # return [word.replace("'","") for word in tweet if (word not in _stopwords and len(word)>= 3)]

    tweet = [word for word in tweet if (word not in _stopwords)]

    # tweet=tagger.tag(tweet)

    return tweet


# Start Program Section :
#
# readAndWriteCorpus(getFullPath('tweetDataFile1.csv'), getFullPath('NON_SARCASM_DEV.txt',True))
# for _fileName in os.listdir(os.path.join(os.getcwd() ,'Data','FetchedData')):
#     print(readAndWriteCorpus(getFullPath(_fileName), getFullPath(_fileName,True)))

from nltk.tag.perceptron import PerceptronTagger

tagger = PerceptronTagger()

# Getting a list for making stop words list.
_stopwords = set(nltk.corpus.stopwords.words('english') + list(punctuation) + ['AT_USER', 'URL', 'sarcasm', 'rt'])
allFileAsList = []
folderName = os.path.join(os.getcwd(), 'Data', 'FetchedData', 'FinalData')
for _file in os.listdir(folderName):
    # Printing fileName being scanned
    # print '-'*100
    # print(_file)
    # print '-'*100

    allFileAsList.append([])

    # Opening file line by line and appending to list.
    with open(getFullPath(_file, True), 'rb') as csvfile:
        lineReader = csv.reader(csvfile, delimiter=',')
        for row in lineReader:
            # allFileAsList[len(allFileAsList)-1].append('fileName : ' + ',' + _file)
            allFileAsList[len(allFileAsList) - 1].append(row[0] + ',' + row[1])

# pro=[]
# for eachList in allFileAsList:
#     #print(eachList[0])   #format:always ,  Reading #zizek before bed is always a recipe for a nice
#     pro=processTweets(_stopwords,eachList)

devData = processTweets(allFileAsList[2])
# testData=processTweets(allFileAsList[3])


for index in range(0, 100):
    print '-' * 50 + ' Sentence ' + '-' * 50
    print str(index+1) + ')' , devData[index]

    print '-' * 50 + ' TextBlob ' + '-' * 50
    sentence = ' '.join(list(devData[index][0]))
    ngrams = (TextBlob(sentence).ngrams(n=3))
    for eachgram in ngrams:
        _eachgramAsSentence = ' '.join(list(eachgram))

        if TextBlob(_eachgramAsSentence).sentiment.polarity > 0:
            polarity = 'pos = ' + str(TextBlob(_eachgramAsSentence).sentiment.polarity)
        elif TextBlob(_eachgramAsSentence).sentiment.polarity > 0:
            polarity = 'neg = ' + str(TextBlob(_eachgramAsSentence).sentiment.polarity)
        else:
            polarity = 'Subj = ' + str(TextBlob(_eachgramAsSentence).sentiment)

        print(_eachgramAsSentence,
                polarity
              )
    # print TextBlob(sentence).sentiment

    print '-' * 50 + ' SentiwordNet ' + '-' * 50
    for eachword in devData[index][0]:
        if len(swn.senti_synsets(eachword)) > 0:
            #if swn.senti_synsets(eachword)[0].obj_score() != 1.0:
            print (
                tagger.tag([eachword]),
                ' pos=' + str(swn.senti_synsets(eachword)[0].pos_score()),
                ' neg=' + str(swn.senti_synsets(eachword)[0].neg_score()),
                ' obj=' + str(swn.senti_synsets(eachword)[0].obj_score())
            )
