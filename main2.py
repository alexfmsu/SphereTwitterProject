import tweepy  # https://github.com/tweepy/tweepy
import csv
import sys


# Twitter API credentials

from config import *


def get_all_tweets2(api, name, full_tweets2, id):
    replies = []

    # for full_tweets in tweepy.Cursor(api.user_timeline, screen_name=name, max_id=id, timeout=999999).items(10):
    # print(full_tweets.id)

    for tweet in tweepy.Cursor(api.search, q='to:'+'alexfmsu', timeout=999999).items(200):
        # for tweet in tweepy.Cursor(api.search, q='from:'+'l0ldbl00d', timeout=999999).items(200):
        # for tweet in tweepy.Cursor(api.search, q='from:'+'l0ldbl00d' + ' ' + 'to:'+'tproger', timeout=999999).items(50):
        # for tweet in tweepy.Cursor(api.search, q='from:'+'l0ldbl00d' + ' ' + 'to:'+'tproger', timeout=999999).items(50):
        # for tweet in tweepy.Cursor(api.search, q='to:'+name + ' -filter:replies', timeout=999999).items(10):
        # print(tweet.author)
        print(tweet.text)
        if hasattr(tweet, 'in_reply_to_status_id_str'):
                # exit(1)
                # if (tweet.in_reply_to_status_id_str == full_tweets.id_str):
                #     replies.append(tweet.text)

                # print("Tweet :", full_tweets.text.translate(non_bmp_map))
            #     for elements in replies:
            #         print("Replies :", elements)
            replies = []
        # exit(0)
    exit(0)


def get_all_tweets(name):

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    replies = []
    non_bmp_map = dict.fromkeys(range(0x10000, 65536), 0xfffd)
    for full_tweets in tweepy.Cursor(api.user_timeline, screen_name=name, timeout=999999).items(10):
        # for full_tweets in tweepy.Cursor(api.user_timeline, screen_name=name, max_id=987692485727137794, timeout=999999).items(10):
        print(full_tweets.id)
        # print(full_tweets.retweeted_status.id)
        # exit(0)
        print("Tweet :", full_tweets.text)
        if hasattr(full_tweets, 'retweeted_status'):
            get_all_tweets2(
                api, 'tproger', full_tweets.retweeted_status, full_tweets.retweeted_status.id)
        # api, 'tproger', full_tweets.retweeted_status, '987692485727137794')
        for tweet in tweepy.Cursor(api.search, q='to:'+name, result_type='recent', timeout=999999).items(10):
            if hasattr(tweet, 'in_reply_to_status_id_str'):
                if (tweet.in_reply_to_status_id_str == full_tweets.id_str):
                    replies.append(tweet.text)

        for elements in replies:
            print("Replies :", elements)
        replies = []


if __name__ == '__main__':
    get_all_tweets("alexfmsu")
    # get_all_tweets("tproger")
