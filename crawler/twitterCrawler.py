import tweepy
import crawler.authenticator as auth
import json
import time
from os.path import join
import os


api = tweepy.API(auth.authenticate(), wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
cursor = tweepy.Cursor(api.search,
                       q='ethereum OR #ethereum',
                       rpp=50,
                       lang='en',
                       # result_typr='recent',
                       include_entities=True).items()
jsonDir = 'resources/rawTweets/ethereumTweets'


def now():
    return int(round(time.time()))


def crawlTwitter(cursor, outputFolder):
    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)

    def newJsonFile():
        """Creates a new Json File and inserts initial Json."""
        print('creating new file')
        f = open(join(outputFolder, 'tweets-' + str(now()) + '.json'), 'a')
        f.write('[\n')
        return f

    def closeJson(f):
        """Closes file and ends Json."""
        print('closing file')
        f.write(']')
        f.close()

    print('writing first tweet')
    # Writes first tweet to the file from the iterator, to prevent trailing Comma
    f = newJsonFile()
    f.write(json.dumps(cursor.next()._json) + '\n')

    print('starting twitter crawl')
    for count, tweet in enumerate(cursor):
        print(count)
        f.write(',' + json.dumps(tweet._json) + '\n')
        if(count % 2500 == 0):
            print('create new file')
            closeJson(f)
            f = newJsonFile()

    print('End of Cursor')
    closeJson(f)


def twitterToCsv(inputfolder, outputFolder):
    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)

    for file in os.listdir(inputfolder):
        print(file)
        # nltk.twitter.common.json2csv


def crawl():
    outputFolder = jsonDir + '_' + str(now())
    crawlTwitter(cursor, outputFolder)
