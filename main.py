import json
import tweepy
import re

consumer_key = 'wezSPSzc1yGR83f6ykGXrSESv'
consumer_secret = 'H91ncZl0u0LugfqCnzeXEZZc4gT6Jp5Ss9zACsQ2lLWuFQVbwP'
access_token = '3064584671-HEsNDU3GcKlLBdL3dxq7t5hAU9RDkZ5MeIRvD78'
access_token_secret = 'o7weRvnH22L7ct3NTVTRK8aMKEGyARZYFjdOQxSLWfDiE'
session = {}

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

try:
    redirect_url = auth.get_authorization_url()
    session['request_token'] = auth.request_token
except tweepy.TweepError:
    print('Error! Failed to get request token.')


request_token = session['request_token']
del session['request_token']

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.request_token = request_token

auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


def collectData(api, user, limit=1):
    tweets = []

    count = 0

    for tweet in tweepy.Cursor(api.user_timeline, screen_name=user).items():
        tweets.append(tweet)

        # print(dir(tweet))
        # print()

        print({
            'author': tweet.author.name,
            'entitties': tweet.entities,
            'hashtags': tweet.entities['hashtags'],
            'favorite_count': tweet.favorite_count,
            'retweeted': tweet.retweeted,
            'retweet_count': tweet.retweet_count,
            'collected_on': tweet.created_at.strftime('%Y-%m-%d'),
            'text': tweet.text,
            'description': re.sub(r'http\S+', '', tweet.text),
        }, "\n")

        count += 1

        if count >= limit:
            break


users = ['tproger']

for user in users:
    collectData(api, user, limit=1)
