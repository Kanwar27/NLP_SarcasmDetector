import csv
import twitter
import re
import os
import sys, traceback

api = twitter.Api(
                    consumer_key = 'YnH8HtrVYhxmNSr4lLLpuI5MG',
                    consumer_secret = 'gk5Je6TJT9Bt2M7lrxask8LYFv0s4l7U2mKEeVUg6I7tvgAFW5',
                    access_token_key = '1571106582-jSTOVFhv7o8AxXiceEv6Sx60njiuUPH0lr77oI8',
                    access_token_secret = 'tE5wzDkRAijVNL5O6vfDQzHzyBWTGlEpvVN9Y6nhGACBz'
                )

def getFullPath(fileName, isOutput=False):
    if(isOutput):
        dir = os.path.join(os.getcwd() ,'Data','FetchedData', 'FinalData', fileName)
    else:
        dir = os.path.join(os.getcwd() ,'Data','FetchedData', fileName)
    return dir


def saveAfterDownload(trainingData, tweetDataFile):
        with open(tweetDataFile, 'w') as csvfile:
            fieldnames = ['Topic', 'Text']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            #writer.writeheader();
            for _eachline in trainingData:
                try:
                    writer.writerow({'Topic': _eachline.split(',')[0].split(':')[1].replace('"',''), 'Text': _eachline.split(',')[1].split(':')[1].replace('"','')})
                except:
                    continue


def readAndWriteCorpus(corpusFile, destFile):
    print(corpusFile)
    print(destFile)
    try:
        corpus=[]
        with open(corpusFile,'rU') as csvfile:
            lineReader = csv.reader(csvfile,delimiter=':')
            for row in lineReader:
                try:
                    corpus.append(row[1].split('\t')[1].strip('"') + ' : ' + row[2].split('\t')[0].strip('"') + ' , ' + row[2].split('\t')[1].strip('"') + ' : ' + '. '.join(row[3:]))
                except:
                    continue
        saveAfterDownload(corpus,destFile)
        print('Successfully written file ' + getFullPath(destFile))
    except:
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60

#readAndWriteCorpus(getFullPath('tweetDataFile1.csv'), getFullPath('NON_SARCASM_DEV.txt',True))
for _fileName in os.listdir(os.path.join(os.getcwd() ,'Data','FetchedData')):
    print(readAndWriteCorpus(getFullPath(_fileName), getFullPath(_fileName,True)))
