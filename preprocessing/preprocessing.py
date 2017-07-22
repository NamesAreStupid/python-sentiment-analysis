import json
import os
from util import pipeline
from nltk.tokenize import TweetTokenizer


def preprocess():
    print('Starting preprocessing.')
    sourceDir = 'resources/rawTweets/ethereumTweets_1498430250/'
    outputFile = 'resources/preprocessing/processedTweets.json'

    pl = pipeline.makePipeline(selectAttributes, tokenizeTweets)
    processedTweets = list(pl(consolidateTweets(sourceDir)))
    print(len(processedTweets), ' tweets processed.')

    with open(outputFile, 'w') as out:
        out.write(json.dumps(processedTweets))


def consolidateTweets(dir):
    for file in os.listdir(dir):
        with open(os.path.join(dir + file)) as f:
            # print(f)
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
    for tweet in tweets:
        yield {attribute: tweet[attribute] for attribute in attributes}
    # return ({attribute: tweet[attribute] for attribute in attributes} for tweet in tweets)


def tokenizeTweets(tweets):
    tknzr = TweetTokenizer()
    for tweet in tweets:
        # tweet['tokenizedText'] = tknzr.tokenize(tweet['text'])
        tweet['text'] = tknzr.tokenize(tweet['text'])
        yield tweet
