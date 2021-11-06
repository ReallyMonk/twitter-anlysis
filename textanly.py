from textblob import TextBlob, blob
import json
import pandas as pd
import numpy as np
import textblob
import csv
import gettweets
import os

orifilepath = "./MFA_China.txt"
infilepath = "./MFA_ChinaRes.json"
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
filelist_path = './lv1Related_full/'


def build_mention_matrix(filelist_path):
    filelist = os.listdir(filelist_path)
    mention_list = []

    # pick up mention list
    for filename in filelist:
        #file_j = json.dumps(filename)
        mention_list.append(filename.split('.')[0])
    print(mention_list)
    print('got {} totally'.format(len(mention_list)))

    # initial matrix
    data = np.zeros((len(mention_list), len(mention_list)))
    mention_mtx = pd.DataFrame(data, columns=mention_list, index=mention_list)
    print(mention_mtx)

    # buil dataframe matrix horizontal axis been source, veritcal axis been target
    for filename in filelist:
        with open(filelist_path + filename, 'r', encoding='utf-8') as f:
            # print(f.readlines())
            source = filename.split('.')[0]
            for twt in f.readlines():
                twt = json.loads(twt)
                for men_user in twt['mentions']:
                    target = men_user['screen_name']
                    if target in mention_list:
                        mention_mtx[source][target] += 1

    mention_mtx.to_csv('./mentions.csv')
    print(mention_mtx)
    return


jsonfile_path = './MFA_China_response_txt.json'

# a tweet object should include:
# username, time, content, tweet_id, media, reply_count, retweet_count, favorite_count, quote_count, mentions, rt_mentions, hashtags


def extract_tweet(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        user_info = None
        for item in lines:
            # get tweets according to timeline
            item = json.loads(item)
            # find the user information
            if not user_info:
                screen_name = filepath.split('./')[1].split('_response')[0]
                # find user in globalObjects.users
                for user in item['globalObjects']['users'].keys():
                    if item['globalObjects']['users'][user]['screen_name'] == screen_name:
                        tar_user = item['globalObjects']['users'][user]
                        continue
                #print(tar_user)
                user_info = {
                    'screen_name': screen_name,
                    'username': tar_user['name'],
                    'user_id': tar_user['id_str'],
                }
            # start extract tweet
            timeline = item['timeline']['instructions'][0]['addEntries']['entries']
            globaltwts = item['globalObjects']['tweets']
            for twt in timeline:
                if twt['entryId'].startswith('tweet-'):
                    twt_id = twt['sortIndex']
                    tweet_tmp = globaltwts[twt_id]
                    # separate tweet or retweet
                    if 'retweeted_status_id_str' in tweet_tmp:
                        is_retweet = True
                        rt_obj = globaltwts[tweet_tmp['retweeted_status_id_str']]
                        # modify content
                        # but notice that some retweet user may not exist, so we need to check if the user still exist
                        if 'user_mentions' in tweet_tmp['entities']:
                            rt_user = tweet_tmp['full_text'].split('@')[1].split(':')[0]
                            content = 'RT @{}: '.format(rt_user) + rt_obj['full_text']
                        mentions = [rt_user]
                        rt_mentions = []
                        if 'user_mentions' in rt_obj['entities']:
                            rt_mentions = [mention['screen_name'] for mention in rt_obj['entities']['user_mentions']]
                        obj = rt_obj
                    else:
                        is_retweet = False
                        content = tweet_tmp['full_text']
                        mentions = []
                        if 'user_mentions' in tweet_tmp['entities']:
                            mentions = [mention['screen_name'] for mention in tweet_tmp['entities']['user_mentions']]
                        rt_mentions = []
                        obj = tweet_tmp

                    retweet_cnt = obj['retweet_count']
                    favorite_cnt = obj['favorite_count']
                    reply_cnt = obj['reply_count']
                    quote_cnt = obj['quote_count']
                    # check media
                    media = []
                    if 'media' in obj['entities']:
                        media = [media_item['type'] for media_item in obj['entities']['media']]
                        media.extend([media_item['type'] for media_item in obj['extended_entities']['media']])
                        media = list(set(media))
                    # check hashtags
                    hashtags = []
                    if 'hashtags' in obj['entities']:
                        hashtags = [hashitem['text'] for hashitem in obj['entities']['hashtags']]

                    tweet = {
                        'time': tweet_tmp['created_at'],
                        'tweet_id': tweet_tmp['id_str'],
                        'is_retweet': is_retweet,
                        'content': content,
                        'media': media,
                        'hashtags': hashtags,
                        'mentions': mentions,
                        'rt_mentions': rt_mentions,
                        'retweet_count': retweet_cnt,
                        'favorite_count': favorite_cnt,
                        'reply_count': reply_cnt,
                        'quote_count': quote_cnt,
                    }
                    tweet.update(user_info)
                    # write tweets to file
                    with open('./MFA_China_new.json', 'a', encoding='utf-8') as out_f:
                        out_f.write(json.dumps(tweet) + '\n')


extract_tweet(jsonfile_path)

#build_mention_matrix(filelist_path)