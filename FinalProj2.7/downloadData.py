import twitter
import time
import csv
import sys

api = twitter.Api(
                    consumer_key = 'YnH8HtrVYhxmNSr4lLLpuI5MG',
                    consumer_secret = 'gk5Je6TJT9Bt2M7lrxask8LYFv0s4l7U2mKEeVUg6I7tvgAFW5',
                    access_token_key = '1571106582-jSTOVFhv7o8AxXiceEv6Sx60njiuUPH0lr77oI8',
                    access_token_secret = 'tE5wzDkRAijVNL5O6vfDQzHzyBWTGlEpvVN9Y6nhGACBz'
                )

corpus1 = []
corpus2 = []
corpus3 = []
corpus4 = []
corpus5 = []
corpus6 = []
corpus7 = []
corpus8 = []
corpus9 = []

trainingData = []

def readCorpus(corpusFile, corpus):
    with open(corpusFile,'rb') as csvfile:
        lineReader = csv.reader(csvfile,delimiter='	')
        for row in lineReader:
            corpus.append({"tweet_id":row[1],"target":row[0]})

def getTextFromCorpus(corpus):
    rate_limit = 180
    sleep_time = 900/180

    for tweet in corpus:
        try:
            status = api.GetStatus(tweet["tweet_id"])
            tweet["text"] = status.text
            print(tweet["tweet_id"] + " : " + tweet["text"])
            trainingData.append(tweet)
            time.sleep(sleep_time) # to avoid being rate limited
        except:
            continue


def saveAfterDownload(trainingData, tweetDataFile):
        # Once the tweets are downloaded write them to a csv, so you won't have to wait 40 hours
        # every time you run this code :)
        with open(tweetDataFile,'wb') as csvfile:
            linewriter=csv.writer(csvfile,delimiter='\t',quotechar="\"")
            for tweet in trainingData:
                try:
                    print("ID : " + tweet["tweet_id"],"Topic : " + tweet["target"],"Text : " + tweet["text"])
                    linewriter.writerow(
                        [
                            "ID : " + tweet["tweet_id"],
                            "Topic : " + tweet["target"],
                            "Text : " + tweet["text"]
                        ]
                    )
                except Exception, e:
                    print e
        # return trainingData

#corpusFile1 = r'E:\NLP_SarcasmDetector\FinalProj2.7\Data\tweet.NON_SARCASM.all.id.DEV'
#corpusFile2 = r'E:\NLP_SarcasmDetector\FinalProj2.7\Data\tweet.NON_SARCASM.all.id.TEST'
#corpusFile3 = r'E:\NLP_SarcasmDetector\FinalProj2.7\Data\tweet.NON_SARCASM.all.id.TRAIN'
corpusFile4 = r'E:\NLP_SarcasmDetector\FinalProj2.7\Data\tweet.SARCASM.all.id.DEV'
corpusFile5 = r'E:\NLP_SarcasmDetector\FinalProj2.7\Data\tweet.SARCASM.all.id.TEST'
#corpusFile6 = r'E:\NLP_SarcasmDetector\FinalProj2.7\Data\tweet.SARCASM.all.id.TRAIN'
corpusFile7 = r'E:\NLP_SarcasmDetector\FinalProj2.7\Data\tweet.SENTIMENT.all.id.DEV'
corpusFile8 = r'E:\NLP_SarcasmDetector\FinalProj2.7\Data\tweet.SENTIMENT.all.id.TEST'
#corpusFile9 = r'E:\NLP_SarcasmDetector\FinalProj2.7\Data\tweet.SENTIMENT.all.id.TRAIN'

#readCorpus(corpusFile1, corpus1)
#readCorpus(corpusFile2, corpus2)
#readCorpus(corpusFile3, corpus3)
readCorpus(corpusFile4, corpus4)
readCorpus(corpusFile5, corpus5)
#readCorpus(corpusFile6, corpus6)
readCorpus(corpusFile7, corpus7)
readCorpus(corpusFile8, corpus8)
#readCorpus(corpusFile9, corpus9)

# print("Reading first corpus !!")
# tweetDataFile1=r'E:\\NLP_SarcasmDetector\\FinalProj2.7\\Data\\FetchedData\\tweetDataFile1.csv'
# getTextFromCorpus(corpus1)
# saveAfterDownload(corpus1 , tweetDataFile1)
#
# print("Reading second corpus !!")
# tweetDataFile2=r'E:\\NLP_SarcasmDetector\\FinalProj2.7\\Data\\FetchedData\\tweetDataFile2.csv'
# getTextFromCorpus(corpus2)
# saveAfterDownload(corpus2 , tweetDataFile2)

# print("Reading third corpus !!")
# tweetDataFile3=r'E:\\NLP_SarcasmDetector\\FinalProj2.7\\Data\\FetchedData\\tweetDataFile3.csv'
# getTextFromCorpus(corpus3)
# saveAfterDownload(corpus3 , tweetDataFile3)

print("Reading fourth corpus !!")
tweetDataFile4=r'E:\\NLP_SarcasmDetector\\FinalProj2.7\\Data\\FetchedData\\tweetDataFile4_again.csv'
getTextFromCorpus(corpus4)
saveAfterDownload(corpus4 , tweetDataFile4)

print("Reading fifth corpus !!")
tweetDataFile5=r'E:\\NLP_SarcasmDetector\\FinalProj2.7\\Data\\FetchedData\\tweetDataFile5_again.csv'
getTextFromCorpus(corpus5)
saveAfterDownload(corpus5 , tweetDataFile5)

# print("Reading sixth corpus !!")
# tweetDataFile6=r'E:\\NLP_SarcasmDetector\\FinalProj2.7\\Data\\FetchedData\\tweetDataFile6.csv'
# getTextFromCorpus(corpus6)
# saveAfterDownload(corpus6 , tweetDataFile6)

print("Reading seventh corpus !!")
tweetDataFile7=r'E:\\NLP_SarcasmDetector\\FinalProj2.7\\Data\\FetchedData\\tweetDataFile7_again.csv'
getTextFromCorpus(corpus7)
saveAfterDownload(corpus7 , tweetDataFile7)

print("Reading eigth corpus !!")
tweetDataFile8=r'E:\\NLP_SarcasmDetector\\FinalProj2.7\\Data\\FetchedData\\tweetDataFile8_again.csv'
getTextFromCorpus(corpus8)
saveAfterDownload(corpus8,tweetDataFile8)

# print("Reading ninth corpus !!")
# tweetDataFile9=r'E:\\NLP_SarcasmDetector\\FinalProj2.7\\Data\\FetchedData\\tweetDataFile9.csv'
# getTextFromCorpus(corpus9)
# saveAfterDownload(corpus9 , tweetDataFile9)