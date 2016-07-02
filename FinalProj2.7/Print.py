import Info
import re
import datetime
import time

def printTime():
    now = datetime.datetime.now()
    return ('Time:' + str(now.hour) + ':' + str(now.minute) + ':' + str(now.second))

query = '#sarcasm'
max_tweets = 100

print("Started searching on website", printTime())

search_results = [status for status in Info.tweepy.Cursor(Info.api.search, q=query).items(max_tweets)]

print("Completed searching", printTime())

print("Started text manipulation and printing", printTime())

final_tweets_set=''

num =1
for i in search_results:
    try:
        final_tweets_set += re.sub(r"[^a-zA-Z0-9 \n\.\)\:\#\@]+", '',
           (
                str(num) + ") "
                + "Name : " + str(i.entities['user_mentions'][0]['name'])
                + ", Twitter Name : " + str(i.entities['user_mentions'][0]['screen_name'])
                + ", Location  : " + str(i._json['user']['location'])
                + ", Status : " + i.text
           )
        ) + '\n'
        #tweet = search_results.next()
    except: #Info.tweepy.TweepError:
        time.sleep(60*15)
        final_tweets_set += re.sub(r"[^a-zA-Z0-9 \n\.\)\:\#\@]+", '',
                                       (
                                           str(num) + ") "
                                           + "Status : " + i.text
                                       )
                                   ) + '\n'
        pass
    num +=1

file_Location ='E:\\test.txt'

f = open(file_Location,'w')#,encoding='utf-8')
f.write(final_tweets_set)
f.close()

print('File written at ' + file_Location)

print("Text manipulation and printing completed", printTime())
