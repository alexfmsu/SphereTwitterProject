import sys
import json
import time
import logging
import twitter
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
import urllib

import config as e

t = twitter.Api(
    consumer_key=e["CONSUMER_KEY"],
    consumer_secret=e["CONSUMER_SECRET"],
    access_token_key=e["ACCESS_TOKEN"],
    access_token_secret=e["ACCESS_TOKEN_SECRET"],
    sleep_on_rate_limit=True
)


def tweet_url(t):
    return "https://twitter.com/%s/status/%s" % (t.user.screen_name, t.id)


def get_tweets(filename):
    for line in open(filename):
        yield twitter.Status.NewFromJsonDict(json.loads(line))


def get_replies(tweet):
    user = tweet.user.screen_name
    tweet_id = tweet.id
    max_id = None
    logging.info("looking for replies to: %s" % tweet_url(tweet))
    while True:
        q = urllib.urlencode({"q": "to:%s" % user})
        try:
            replies = t.GetSearch(
                raw_query=q, since_id=tweet_id, max_id=max_id, count=20)
            logging.info("size of replies == %s" % len(replies))
        except twitter.error.TwitterError as e:
            logging.error("caught twitter api error: %s", e)
            time.sleep(60)
            continue
        for reply in replies:
            logging.info("examining: %s" % tweet_url(reply))
            if reply.in_reply_to_status_id == tweet_id:
                logging.info("found reply: %s" % tweet_url(reply))
                yield reply
                # recursive magic to also get the replies to this reply
                for reply_to_reply in get_replies(reply):
                    yield reply_to_reply
            max_id = reply.id
        if len(replies) != 100:
            break


if __name__ == "__main__":
    logging.basicConfig(filename="replies.log", level=logging.INFO)
    tweets_file = []
    tweets_file.append(t.GetStatus("909922763774861314"))
    for tweet in tweets_file:
        for reply in get_replies(tweet):
            print(reply.AsJsonString())
