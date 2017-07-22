import os
import json

rootDir = 'resources/rawTweets/ethereumTweets_1498430250/'
# rootDir = 'resources/rawTweets/ethereumTweets_1498497369/'
idDict = {}
print('Checkign dir for duplicate tweets: ' + rootDir)
for file in os.listdir(rootDir):
    with open(os.path.join(rootDir + file)) as f:
        # print(f)
        try:
            tweetJson = json.load(f)
            for tweet in tweetJson:
                tid = tweet['id']
                if tid in idDict:
                    idDict[tid] += 1
                else:
                    idDict[tid] = 1
        except json.decoder.JSONDecodeError as err:
            print('Couldnt load json from file {0}'.format(f.name))
            print(err)
        except Exception as err:
            print(err)

duplicates = [(tid, count) for tid, count in idDict.items() if count >= 2]
if(len(duplicates) > 0):
    print(duplicates)
else:
    print('No duplicates found.')
