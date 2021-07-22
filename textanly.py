from textblob import TextBlob, blob
import json
import pandas as pd
import numpy as np
import textblob

filepath = "./MFA_ChinaRes.json"
ofilepath = "./MFA_China_Label.json"


# relabel the tweets info according to some key words
def relabel_tweets():
    # pick up all labels
    exist_labels = []
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        for jsonstr in f.readlines():
            jsonstr = json.loads(jsonstr)

            for label in jsonstr['label']:
                if label not in exist_labels:
                    exist_labels.append(label)

    print('totally got total {} labels'.format(len(exist_labels)))
    if 'rest' in exist_labels:
        print(True)

    # set new label to tweet if tweet not been labeled before
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        for jsonstr in f.readlines():
            jsonstr = json.loads(jsonstr)
            if 'rest' in jsonstr['label']:
                new_label = []
                # check if there is keyswords in tweet
                for label in exist_labels:
                    if jsonstr['tweet'].find(label) != -1:
                        print(jsonstr['tweet'].find(label))
                        new_label.append(label)
                # if still no label then wirte rest
                if new_label == []:
                    new_label = ['rest']
                new_tweet = {"tweet": jsonstr['tweet'], "label": new_label}
                #break
            else:
                new_tweet = jsonstr

            with open(ofilepath, 'a') as new_f:
                json.dump(new_tweet, new_f)
                new_f.write('\n')

    print('relabel done')


# fetch tweets from file
def content_analysis():
    tt_polarity = []
    tt_subjectivity = []
    tt_category = []
    with open(ofilepath, 'r', encoding='utf-8', errors='ignore') as f:
        for jsonstr in f.readlines():
            jsonstr = json.loads(jsonstr)

            tweet = jsonstr['tweet']
            labels = jsonstr['label']

            # get the score
            blob = TextBlob(tweet)
            polarity = blob.sentiment[0]
            subjectivity = blob.sentiment[1]
            #print(polarity, subjectivity)

            for label in labels:
                tt_polarity.append(polarity)
                tt_subjectivity.append(subjectivity)
                tt_category.append(label)

    #print(len(tt_polarity))
    #print(len(tt_subjectivity))
    return tt_polarity, tt_subjectivity, tt_category


#content_analysis()
#relabel_tweets()
#a, b, c = content_analysis()
#print(a, b, c)
