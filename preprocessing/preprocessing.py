import json
import os
from util.pipeline import makePipeline
from nltk.tokenize import TweetTokenizer
from nltk import pos_tag
from functools import reduce


def preprocess():
    print('Starting preprocessing.')
    sourceDir = 'resources/rawTweets/gotTweets_1498248795/'
    outputFile = 'resources/preprocessing/processedTweets.json'

    consolidatedTweets = consolidateTweets(sourceDir)

    pl = makePipeline(selectAttributes, tokenizeTweets)
    processedTweets = list(pl(consolidatedTweets))

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


def posTag(tweet):
    pass
