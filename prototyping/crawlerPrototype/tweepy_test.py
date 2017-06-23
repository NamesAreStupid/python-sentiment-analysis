import tweepy
import authenticator as auth
import json
import time
from os.path import join

api = tweepy.API(auth.authenticate(), wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
cursor = tweepy.Cursor(api.search,
                       q='Star Trek',
                       rpp=50,
                       lang='en',
                       result_typr='recent',
                       include_entities=True).items()
jsonDir = 'tngTweets'


def now():
    return int(round(time.time()))


def checkRls():
    """Checks rate_limit_status of Twitter Search API and returns its value."""
    return api.rate_limit_status()['resources']['search']['/search/tweets']['remaining']


def writeTweets(cursor):
    # tweets = [tweet._json for tweet in cursor].sort(key=lambda x: x["id"])
    count = 1
    tweets = []
    for tweet in cursor:
        print(count)
        count += 1
        tweets.append(tweet._json)
    with open(join('tngTweets', 'tweets' + str(now()) + '.json'), 'w') as f:
        f.write(json.dumps(tweets))


def writeTweetsOld(cursor):
    tweets = [tweet._json for tweet in cursor].sort()
    with open('tweets.json', 'w') as f:
        f.write(json.dumps(tweets))


def writeTweetsAppend(cursor):
    with open('tweets2.json', 'w') as f:
        f.write("[")
    with open('tweets2.json', 'a') as f:
        notFirst = False
        for tweet in cursor:
            if notFirst:
                f.write(',' + json.dumps(tweet._json))
            else:
                f.write(json.dumps(tweet._json))
                notFirst = True
        f.write(']')


def writeTweetsRaw(cursor):
    with open(join('tngTweets', 'tweetsRaw-' + str(now()) + '.json'), 'a') as f:
        count = 1
        for tweet in cursor:
            print(count)
            count += 1
            f.write(json.dumps(tweet._json) + '\n')


def writeTweetsRawFormatted(cursor):
    with open(join('tngTweets', 'tweetsRaw-' + str(now()) + '.json'), 'a') as f:
        f.write('[\n')
        f.write(json.dumps(cursor.next()._json) + '\n')
        count = 1
        for tweet in cursor:
            print(count)
            count += 1
            f.write(',' + json.dumps(tweet._json) + '\n')
        f.write(']')


def crawlTwitter(cursor):
    rootFolder = jsonDir + str(now())
    count = 1

    def newJsonFile():
        """Creates a new Json File and inserts initial Json."""
        nonlocal currentFile
        currentFile = join(rootFolder, 'tweetsRaw-' + str(now()) + '.json')
        f = open(currentFile)
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
        print(count)
        print(checkRls)
        count += 1
        f.write(',' + json.dumps(tweet._json) + '\n')
        if(checkRls == 0):
            closeJson(f)
            f = newJsonFile()

    closeJson(f)


writeTweetsRaw(cursor)
