import json
import os
from util import pipeline
from nltk.tokenize import TweetTokenizer
from nltk import pos_tag
from functools import reduce


def preprocess():
    print('Starting preprocessing.')
    sourceDir = 'resources/rawTweets/gotTweets_1498248795/'
    outputFile = 'resources/preprocessing/processedTweets.json'

    # pl = pipeline.makeFunctionalPipeline(selectAttributes, tokenizeTweets)
    consolidated = consolidateTweets(sourceDir)
    # plined = pl(consolidated)
    # processedTweets = list(plined)

    # processedTweets = list(map(reduce(lambda x, y: x(y), [selectAttributes, tokenizeTweets]), consolidated))
    # processedTweets = list(map(lambda x: tokenizeTweets(selectAttributes(x)), consolidated))
    # processedTweets = list(map(lambda x: reduce(lambda y, z: z(y), [tokenizeTweets, selectAttributes], x), consolidated))

    pl = pipeline.makePipeline(selectAttributes, tokenizeTweets)
    processedTweets = list(pl(consolidated))

    print(len(processedTweets), ' tweets processed.')

    with open(outputFile, 'w') as out:
        out.write(json.dumps(processedTweets))


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


def selectAttributes(tweet):
    attributes = ['text']
    return {attribute: tweet[attribute] for attribute in attributes}


def tokenizeTweets(tweet):
    tknzr = TweetTokenizer()
    tweet['text'] = tknzr.tokenize(tweet['text'])
    return tweet


def posTag(tweets):
    pass
