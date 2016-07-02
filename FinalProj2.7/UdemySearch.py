import sys
import twitter

consumer_key = 'YnH8HtrVYhxmNSr4lLLpuI5MG'
consumer_secret = 'gk5Je6TJT9Bt2M7lrxask8LYFv0s4l7U2mKEeVUg6I7tvgAFW5'
access_token = '1571106582-jSTOVFhv7o8AxXiceEv6Sx60njiuUPH0lr77oI8'
access_secret = 'tE5wzDkRAijVNL5O6vfDQzHzyBWTGlEpvVN9Y6nhGACBz'

api = twitter.Api(consumer_key,
                  consumer_secret,
                  access_token,
                  access_secret)

#print(api.VerifyCredentials())


def createTestData(search_string):
    try:
        tweets_fetched = api.GetSearch(search_string, count=100)
        print("Great! We fetched " + str(len(tweets_fetched)) + " tweets with the term " + search_string + "!!")
        return [{"Text": status.text, "label:": None} for status in tweets_fetched]
    except:
        print(sys.exc_info())
        #return None

#search_string= input("Hi there! What are we searching today ?")


testData = createTestData("#sarcasm")
print(testData)
