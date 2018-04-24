import json
import tweepy
import csv
import re

from config import *

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

auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)


def write_csv(path, filename, DATA):
    with open(path+'/'+filename, 'w') as csvfile:
        fieldnames = DATA[0].keys()
        # fieldnames = ['first_name', 'last_name']

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for i in DATA:
            writer.writerow(i)

        # writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})
        # writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
        # writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})


def get_words(text):
    text = text.replace("\n", " ")
    text = text.replace(",", "").replace(
        ".", "").replace("?", "").replace("!", "")
    text = text.lower()
    words = text.split()
    words.sort()
    return words


def get_words_dict(words):
    words_dict = dict()

    for word in words:
        if word in words_dict:
            words_dict[word] = words_dict[word] + 1
        else:
            words_dict[word] = 1
    return words_dict


def collectData(api, user, limit=1, path='data'):
    tweets = []

    count = 0
    DATA = []
    # write_csv()

    for tweet in tweepy.Cursor(api.user_timeline, screen_name=user).items():
        tweets.append(tweet)

        # print(dir(tweet))
        # print()

        # print({
        #     'author': tweet.author.name,
        #     'entitties': tweet.entities,
        #     'hashtags': tweet.entities['hashtags'],
        #     'favorite_count': tweet.favorite_count,
        #     'retweeted': tweet.retweeted,
        #     'retweet_count': tweet.retweet_count,
        #     'collected_on': tweet.created_at.strftime('%Y-%m-%d'),
        #     'text': tweet.text,
        #     'description': re.sub(r'http\S+', '', tweet.text),
        # }, "\n")

        data = {}

        data['author'] = tweet.author.name
        data['like_count'] = tweet.favorite_count
        data['retweet_count'] = tweet.retweet_count
        data['retweeted'] = tweet.retweeted
        data['hashtags_count'] = len(tweet.entities['hashtags'])
        data['created'] = str(tweet.created_at.strftime('%Y-%m-%d'))

        data['symbol_cnt'] = len(tweet.text)
        # data['text'] = tweet.text

        words = get_words(tweet.text)
        # data['words'] = words
        data['words_cnt'] = len(words)

        uniq_words = get_words_dict(words)
        # data['uniq_words'] = uniq_words
        data['uniq_words_cnt'] = len(uniq_words)

        DATA.append(data)

        count += 1

        if count >= limit:
            break

    write_csv(path, user+'.csv', DATA)


# users = [
#     'novaya_gazeta‏',
#     'tvrain',
#     'snob_project',
#     'meduzaproject‏',
#     'znak_com'
# ]

users = [
    'novaya_gazeta',
    'tvrain',
    'snob_project',
    'meduzaproject',
    'znak_com',
]

for user in users:
    collectData(api, user, limit=10, path='data')
