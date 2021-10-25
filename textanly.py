from textblob import TextBlob, blob
import json
import pandas as pd
import numpy as np
import textblob
import csv
import gettweets

orifilepath = "./MFA_China.txt"
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
    return


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


# seperate tweets into clusters according to hastags they have
def seperate_hastag(txt_f):
    # get files and collected hashtags
    tag_list = {}
    with open(txt_f, 'r', encoding='utf-8', errors='ignore') as f:
        #f = json.load(f)
        for jsonstr in f.readlines():
            #print(jsonstr)
            jsonstr = json.loads(jsonstr)
            # fetch new tags from json item
            #print(jsonstr)
            for tag in jsonstr['hashtags']:
                if tag not in tag_list:
                    tag_list[tag] = []
                # add tweet into tag filter
                tag_list[tag].append(jsonstr['date'] + '  ' + jsonstr['tweet'])
        f.close()
        # write into files
    #print('here')
    tag_order = {}
    for tag in tag_list:
        tag_count = len(tag_list[tag])
        tag_order[tag] = len(tag_list[tag])
        tmp_out_file_path = "./MFA_China/{}-{}.txt".format(tag, tag_count)
        with open(tmp_out_file_path, 'a', encoding='utf-8', errors='ignore') as f:
            #for content in tag_list[tag]:
            #f.write(content + '\n')
            f.close()
    tag_order = sorted(tag_order.items(), key=lambda kv: (-kv[1], kv[0]))
    with open('./tag_order.csv', 'a', encoding='utf-8') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(['tag', 'count'])
        #for item in tag_order:
        csv_writer.writerows(tag_order)

    return


#print(gettweets.get_mention_users())