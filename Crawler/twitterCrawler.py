import tweepy
import crawler.authenticator as auth
import json
import time
from os.path import join
import os

api = tweepy.API(auth.authenticate(), wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
cursor = tweepy.Cursor(api.search,
                       q='#tng',
                       rpp=50,
                       lang='en',
                       result_typr='recent',
                       include_entities=True).items()
jsonDir = 'resources/rawTweets/tngTweets'


def now():
    return int(round(time.time()))


def crawlTwitter(cursor):
    rootFolder = jsonDir + '_' + str(now())
    if not os.path.exists(rootFolder):
        os.makedirs(rootFolder)

    count = 1

    def newJsonFile():
        """Creates a new Json File and inserts initial Json."""
        f = open(join(rootFolder, 'tweets-' + str(now()) + '.json'), 'a')
        f.write('[\n')
        return f

    def closeJson(f):
        """Closes file and ends Json."""
        f.write(']')
        f.close()

    # Writes first tweet to the file from the iterator, to prevent trailing Comma
    f = newJsonFile()
    f.write(json.dumps(cursor.next()._json) + '\n')

    for tweet in cursor:
        count += 1
        f.write(',' + json.dumps(tweet._json) + '\n')
        if(count % 1000 == 0):
            print(count)
            closeJson(f)
            f = newJsonFile()

    closeJson(f)


def crawl():
    crawlTwitter(cursor)
