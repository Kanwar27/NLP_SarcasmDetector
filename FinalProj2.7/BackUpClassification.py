# region Import Statements
import re
import csv
import os, time
from collections import defaultdict
import sys, traceback
import nltk
# from nltk.tag.perceptron import PerceptronTagger
from string import punctuation
from nltk.corpus import sentiwordnet as swn
from textblob import TextBlob
from nltk.tokenize import TweetTokenizer
# from nltk.stem.porter import *
# import enchant

# from autocorrect import spell
# import itertools

# endregion


_stopwords = []
# stemmer = PorterStemmer()
# en_US_dict = enchant.Dict("en_US")
symbol = '='
# tagger = PerceptronTagger()
tknzr = TweetTokenizer()

# Getting a list for making stop words list.
_stopwords = set(
                    nltk.corpus.stopwords.words('english') + list(punctuation) +
                    ['AT_USER', 'URL', 'sarcasm', 'rt', 'since', 'anyways']
                )

# region Functions Inside
# Convert timedelta into hour:min:sec format
def days_hours_minutes(td):
    return td.days, td.seconds//3600, (td.seconds//60)%60

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
    #print(corpusFile)
    #print(destFile)
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
        print symbol * 60
        traceback.print_exc(file=sys.stdout)
        print symbol * 60


# First processing of Tweets but the data needs to be sent as list parameter.
def processTweets(list_of_tweets):
    # The list of tweets is a list of dictionaries which should have the keys, "text" and "label"
    processedTweets = []
    # This list will be a list of tuples. Each tuple is a tweet which is a list of words and its label
    for tweet in list_of_tweets:
        processedTweets.append((_processTweet(tweet.split(',')[1]), tweet.split(',')[0]))
    return processedTweets


# Trying to replace some common Slangs :
# Could have used a Slang dictionary from internet and replaced each word with correct spelling.
# Too much overhead so avoiding , replaced some words and for rest checked spellings and omitted the word if
# spellings are not correct. Used "pyenchant" for that.

def customReplaceFunc(list_word):
    dicToReplace = {
        "it's": 'it is',
        "'ve": 'have',
        "'re": 'are',
        "ya": '',
        "u": 'you',
        "'re": 'are',
        "'d": 'would',
        "'s": 'is',
        "'m": 'am',
        "'t": 'not',
        "n't": 'not',
        "ur": 'you are',

        # unncessary
        "amp": '',
        "yay": '',
        "ya": ''
    }

    # print ['Original'] + list_word
    for index in range(0, len(list_word)):
        if (dicToReplace.has_key(list_word[index])):
            list_word[index] = dicToReplace.get(str(list_word[index]))
        elif "'" in list_word[index]:
            if (dicToReplace.has_key("'" + list_word[index].split("'")[1])):
                list_word[index] = list_word[index].split("'")[0] + ' ' + dicToReplace.get(
                    "'" + list_word[index].split("'")[1])
    return list_word


# Second processing of Tweets
# Main processing of Tweets....
def _processTweet(tweet):
    # 1. Convert to lower case
    tweet = tweet.lower()

    # 2. Replace links with the word URL
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', tweet)
    # 3. Replace @username with "AT_USER"
    tweet = re.sub('@[^\s]+', 'AT_USER', tweet)
    # 4. Replace #word with word
    # tweet = re.sub(r'#([^\s]+)', r'\2', tweet)

    tweet = re.sub(r'#([^\s]+)', '',
                   tweet)  # used this instead and completely omitted hashtags, most of the times teh hashtags
    # were sarcasm or words like that so no need to include such words

    # 5. Replace any numeric number
    tweet = re.sub('\d', '', tweet)
    # 6. Replace special characters
    tweet = re.sub(r'[,!.;?]', '', tweet)
    #  7. Tokenize word using nltk
    # tweet = nltk.word_tokenize(tweet)
    #  8. Let's now return this list minus any stopwords
    # tweet = [word for word in tweet if (word not in _stopwords)]

    # Did the tagging later inside SentiwordNet when we will have separate words.
    # tweet=tagger.tag(tweet)

    return tweet


# Processing the Training Data using TextBlob, SentiwordNet
def processingDataForSelfUnderStanding(dataSet):
    for index in range(0, dataSet.__len__()):

        print symbol * 50 + ' Sentence ' + symbol * 50

        # Printing Original Sentence
        #print str(index + 1) + ')', str(dataSet[index][0])

        # Tokenizing the sentence
        tokens = tknzr.tokenize(dataSet[index][0])

        # print('tokens : ', tokens)

        # Doing custom Filtering on certain Slangs and words
        customFilteredTokens = customReplaceFunc(tokens)

        # print('customFilteredTokens : ', customFilteredTokens)

        #customFilteredTokens = tknzr.tokenize(' '.join(customFilteredTokens))

        # Removing Stop Words
        afterRemovingStopWords = [word for word in customFilteredTokens if (word not in _stopwords)]

        # print(' afterRemovingStopWords : ', afterRemovingStopWords)

        # time.sleep(40)

        # region Spell - Check of Tokens and Return a sentence
        sentence = ''  # capture the new sentence after spelling check is done on each word
        omitted = ''  # capture the omitted words from each sentence

        # for wrd in afterRemovingStopWords:
        #     if wrd != '':
        #         _isCorrect = en_US_dict.check(wrd)
        #         if _isCorrect:
        #             sentence += wrd + ' '
        #         # Just to see what has been ommitted uncomment the following lines.
        #         else:
        #             omitted += wrd + ' , '
        #             # print('omitted : ' + omitted) if omitted != "" else ''
        #sentence = str(sentence)

        # print('sentence : ', str(sentence))
        # endregion

        # region TextBlob
        print symbol * 50 + ' TextBlob ' + symbol * 50

        ngrams = (TextBlob(sentence).ngrams(n=2))
        for eachgram in ngrams:
            _eachgramAsSentence = ' '.join(list(eachgram))

            if (TextBlob(_eachgramAsSentence).sentiment.polarity + TextBlob(_eachgramAsSentence).sentiment.subjectivity) > 0:
                if TextBlob(_eachgramAsSentence).sentiment.polarity > 0:
                    polarity = (TextBlob(_eachgramAsSentence).sentiment.polarity)  # + (' Subj=' + str(TextBlob(_eachgramAsSentence).sentiment.subjectivity) if TextBlob(_eachgramAsSentence).sentiment.subjectivity > 0 else '')
                elif TextBlob(_eachgramAsSentence).sentiment.polarity < 0:
                    polarity = -(TextBlob(_eachgramAsSentence).sentiment.polarity)  # + (' Subj=' + str(TextBlob(_eachgramAsSentence).sentiment.subjectivity) if TextBlob(_eachgramAsSentence).sentiment.subjectivity > 0 else '')
                # else:
                #     polarity = 'Subj = ' + str(TextBlob(_eachgramAsSentence).sentiment)

                #print(_eachgramAsSentence, polarity)

        # endregion

        # region SentiwordNet
        print symbol * 50 + ' SentiwordNet ' + symbol * 50

        for eachword in dataSet[index][0].split(' '):
            # _stemmedWord = stemmer.stem(eachword)

            # region Tried Spelling Correction
            '''

            # Trying to correct spellings but operations are too costly and mostly the words are
            # subjective so no point henceforth omitting words that are not spelled correctly

            # Replace same characters in a string

            _ReplacedRepitition = ''.join(c for c, _ in itertools.groupby(eachword))



            print('Original : {4} | {0} as {1} / {2} Correct : {3}'.format(_ReplacedRepitition,_correctlySpelledTB, _correctlySpelledAC, _isCorrect, eachword))

            print(_ReplacedRepitition)
            '''
            # endregion

            # if len(swn.senti_synsets(_stemmedWord)) > 0:
            #     subjectivity = swn.senti_synsets(_stemmedWord)[0].pos_score() if swn.senti_synsets(_stemmedWord)[0].pos_score() > swn.senti_synsets(_stemmedWord)[0].neg_score() else -(swn.senti_synsets(_stemmedWord)[0].neg_score())
            #     if swn.senti_synsets(_stemmedWord)[0].obj_score() != 1:
            #         print(tagger.tag([_stemmedWord]) , subjectivity)
                        #     # , ' pos=' + str(swn.senti_synsets(_stemmedWord)[0].pos_score())
                        #     # , ' neg=' + str(swn.senti_synsets(_stemmedWord)[0].neg_score())
                        #     # , ' obj=' + str(swn.senti_synsets(_stemmedWord)[0].obj_score())


        # endregion

        # region
        print('')
        # endregion


def preProcessTweets(dataSet):
    pptrainingData=[]
    for index in range(0, len(dataSet)):
        try:
            # Encoding in utf-8 format
            text = unicode(dataSet[index][0], 'utf-8')
            label = unicode(dataSet[index][1], 'utf-8')
        except:
            print(dataSet[index][0])

        # Tokenizing the sentence
        tokens = tknzr.tokenize(text)

        # Doing custom Filtering on certain Slangs and words
        customFilteredTokens = customReplaceFunc(tokens)

        #After replacing I have in one words two words ex. It's has become It is. Two words in one so tokenizing again.
        customFilteredTokens = tknzr.tokenize(' '.join(customFilteredTokens))

        # Removing Stop Words
        afterRemovingStopWords = [word for word in customFilteredTokens if (word not in _stopwords)]

        # SubjectiveWordsList=[]
        # for eachword in afterRemovingStopWords:
            # _stemmedWord = stemmer.stem(eachword)
            #
            # if len(swn.senti_synsets(_stemmedWord)) > 0:
            #     subjectivity = swn.senti_synsets(_stemmedWord)[0].pos_score() if swn.senti_synsets(_stemmedWord)[0].pos_score() > swn.senti_synsets(_stemmedWord)[0].neg_score() else -(swn.senti_synsets(_stemmedWord)[0].neg_score())
            #     # if swn.senti_synsets(_stemmedWord)[0].obj_score() != 1:
            #     #     print(tagger.tag([_stemmedWord]) , subjectivity)
        SubjectiveWordsDic = dict([(word,True) for word in afterRemovingStopWords])
            # SubjectiveWordsList.append(eachword)
        #topic if required in dataset[index][1]
        #if SubjectiveWordsList != []:
        pptrainingData.append((SubjectiveWordsDic,label))
    return pptrainingData

# def buildingDict(ppTrainingData):
#     all_words=[]
#     for (words,sentiment) in ppTrainingData:
#         all_words.extend(words)
#     # This will give us a list in which all the words in all the tweets are present
#     # These have to be de-duped. Each word occurs in this list as many times as it
#     # appears in the corpus
#     wordlist=nltk.FreqDist(all_words)
#     # This will create a dictionary with each word and its frequency
#     word_features=wordlist.keys()
#     # This will return the unique list of words in the corpus
#     return word_features
#
# def extract_features(tweet):
#     _temp_list_OfSentence = tweet.split(' ')
#     tweet_words=set(_temp_list_OfSentence)
#     features={}
#     for word in word_features:
#         features['contains(%s)' % word]=(word in tweet_words)
#         # This will give us a dictionary , with keys like 'contains word1' and 'contains word2'
#         # and values as True or False
#     return features

# region Reading each file from required Folder path ./Data/FetchedData/FinalData
allFileAsList = []
def readFilesFromDirectory(folderPath, fileNames=[]):

    for _file in os.listdir(folderPath):
        # Printing fileName being scanned
        # print symbol*100
        # print(_file)
        # print symbol*100

        if fileNames.__contains__(_file):
            allFileAsList.append([])

            # f = open(getFullPath(_file, True), 'rb')
            # data = f.read()
            # first_line = data.split('\n', 1)[0]
            #
            # separator = ''
            # if ',' in first_line:
            #     separator=','
            # else:
            #     separator=':'

            # Opening file line by line and appending to list.
            with open(getFullPath(_file, True), 'rb') as csvfile:
                lineReader = csv.reader(csvfile, delimiter=',')
                for row in lineReader:
                    # allFileAsList[len(allFileAsList)-1].append('fileName : ' + ',' + _file)
                    allFileAsList[len(allFileAsList) - 1].append(row[0] + ',' + row[1])

    # endregion
# endregion
# endregion

### Main

folderPath = os.path.join(os.getcwd(), 'Data', 'FetchedData', 'FinalData')
fileNames=['tweet.SARCASM.all.id.TEST.csv','tweet.SARCASM.all.id.TRAIN.csv',
           'tweet.NON_SARCASM.all.id.TEST.csv','tweet.NON_SARCASM.all.id.TRAIN.csv']

Start = time.time()
print("Started reading...")

readFilesFromDirectory(folderPath, fileNames)

Took = time.time() - Start
print ("Took " + str(round(Took,2)) + " to read all files")

# Dividing data in trainingData and testData according to respective files

for _file in allFileAsList:
    if _file[0].__eq__('   always ,  if you ask me what i want the answer will always be some good weed and some good head'):
        testNonSarData = _file
    if _file[0].__contains__("It's so annoying walking in the hallway n"):
        trainNonSarData = _file
    if _file[0].__contains__('Reading #zizek before bed is always a recipe'):
        testSarData = _file
    if _file[0].__contains__("things just don't happen randomly. there"):
        trainSarData = _file

print "Started Dividing into emotion, tweet format"
Start = time.time()

testSarData = processTweets(testSarData[:1500])
testNonSarData = processTweets(testNonSarData)[:1500]
trainSarData = processTweets(trainSarData[:3500])
trainNonSarData = processTweets(trainNonSarData[:3500])

# testNonSarData = processTweets(testSarData[:1500])
# testSarData = processTweets(testNonSarData)[:1500]
# trainNonSarData = processTweets(trainSarData[:3000])
# trainSarData = processTweets(trainNonSarData[:3000])


print("Records took :" + str(time.time() - Start))

#processingDataForSelfUnderStanding(trainingData);

testData= testSarData + testNonSarData

TotalTestDataRec  = len(testData)

print("Records in test Data : " + str(TotalTestDataRec))

Start = time.time()
print("Started processing...")

sarFeat = preProcessTweets(trainSarData)
nonSarFeat = preProcessTweets(trainNonSarData)

trainFeat = sarFeat + nonSarFeat
testFeat = preProcessTweets(testData)

#word_features = buildingDict(tweetProcessor)

#trainingFeatures=nltk.classify.apply_features(extract_features,trainData)

# print(trainingFeatures)

NBayesClassifier=nltk.NaiveBayesClassifier.train(trainFeat)

#NBResultLabels=[NBayesClassifier.classify(extract_features(tweet[0])) for tweet in testData]

print(nltk.classify.util.accuracy(NBayesClassifier, testFeat))

NBayesClassifier.show_most_informative_features()
# print(NBResultLabels)

# if NBResultLabels.count('positive')>NBResultLabels.count('negative'):
# print "NB Result Sarcastic Sentiment\t\t:" + str(100*NBResultLabels.count('sarcasm')/len(NBResultLabels))+"%"
# else:
# print "NB Result Non-Sarcastic Sentiment\t:" + str(100*NBResultLabels.count('non-sarcasm')/len(NBResultLabels))+"%"


