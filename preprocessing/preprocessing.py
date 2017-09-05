import json
import os
from util.pipeline import makePipeline
from nltk.tokenize import TweetTokenizer
from nltk import pos_tag
from functools import reduce
from nltk.stem.porter import *


def preprocess():
    print('Starting preprocessing.')

    sourceDir = 'resources/rawTweets/gotTweets_1498248795/'
    outputFile = 'resources/preprocessing/processedTweets.json'

    consolidatedTweets = consolidateTweets(sourceDir)

    pl = makePipeline(selectAttributes,
                      tokenizeTweets,
                      posTag)
    # processedTweets = list(pl(consolidatedTweets))

    # print(len(processedTweets), ' tweets processed.')

    with open(outputFile, 'w') as out:
        # out.write(json.dumps(processedTweets))
        # print(next(consolidatedTweets)['text'])
        # print(reduce(lambda txt, tweet: txt + tweet['text'] + '\n', consolidatedTweets, ''))
        # out.write(reduce(lambda txt, tweet: txt + tweet['text'] + '\n', consolidatedTweets, ''))
        out.write(reduce(lambda txt, tweet: txt + json.dumps(tweet['text'])[1:-1] + '\n', consolidatedTweets, ''))
        # for tweet in consolidatedTweets:
        #     out.write(json.dumps(tweet['text'])[1:-1] + '\n')

    print('Finished preprocessing.')


def consolidateTweets(dir):
    for file in os.listdir(dir):
        with open(os.path.join(dir + file)) as f:
            try:
                tweetJson = json.load(f)
                for tweet in tweetJson:
                    yield tweet
            except json.decoder.JSONDecodeError as err:
                print('Couldnt load json from file {0}'.format(f.name))
                print(err)
            except Exception as err:
                print(err)


def selectAttributes(tweets):
    attributes = ['text']
    # return ({attribute: tweet[attribute] for attribute in attributes} for tweet in tweets)
    return map(lambda tweet: {attribute: tweet[attribute] for attribute in attributes}, tweets)


def tokenizeTweets(tweets):
    tknzr = TweetTokenizer()
    # return (tweet['text'] = tknzr.tokenize(tweet['text']) for tweet in tweets)
    # return map(lambda tweet: tweet.update(text = tknzr.tokenize(tweet['text'])), tweets)
    for tweet in tweets:
        tweet['text'] = tknzr.tokenize(tweet['text'])
        yield tweet


def posTag(tweets):
    for tweet in tweets:
        tweet['text'] = pos_tag(tweet['text'])
        yield tweet
