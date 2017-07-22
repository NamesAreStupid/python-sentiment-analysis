import nltk
import json
import os


def tokenize(inputDir, outputFile):
    for file in os.listdir(inputDir):
        with open(os.path.join(inputDir + file)) as f:
            # print(f)
            try:
                tweetJson = json.load(f)
                for tweet in tweetJson:
                    pass
            except json.decoder.JSONDecodeError as err:
                print('Couldnt load json from file {0}'.format(f.name))
                print(err)
            except Exception as err:
                print(err)


tokenize('', '')