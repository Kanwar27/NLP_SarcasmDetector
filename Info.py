import tweepy
from tweepy import OAuthHandler

consumer_key = 'YnH8HtrVYhxmNSr4lLLpuI5MG'
consumer_secret = 'gk5Je6TJT9Bt2M7lrxask8LYFv0s4l7U2mKEeVUg6I7tvgAFW5'
access_token = '1571106582-jSTOVFhv7o8AxXiceEv6Sx60njiuUPH0lr77oI8'
access_secret = 'tE5wzDkRAijVNL5O6vfDQzHzyBWTGlEpvVN9Y6nhGACBz'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)

# Creates the user object. The me() method returns the user whose authentication keys were used.
user = api.me()

#print('Name: ' + user.name)
#print('Location: ' + user.location)
#print('Friends: ' + str(user.friends_count))

"""
#get our own twitter tweets
for status in tweepy.Cursor(api.home_timeline).items(100):
    # Process a single status
    print(status.text)
"""




