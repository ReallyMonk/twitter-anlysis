import twint
import json
import os
'''
ERROR: User been defined nonetype
solved by executing following
pip3 install --upgrade -e git+https://github.com/twintproject/twint.git@origin/master#egg=twint
'''

userList = ["MFA_China"]  #,"CHN_UN_NY","zlj517","SpokespersonCHN","ChinaEUMission","China2ASEAN","AmbCuiTiankai","chianscio"]#,"gZclW78FYo7XYMO","China2ASEAN", "MFA_China2", "libijian2", "AmbCuiTiankai", "ChineseEmbinUS"]
mediaList = ["CGTNOfficial", "PDChina", "XHNews"]
kwList = [""]


def fetch_tweet(user):
    c = twint.Config()
    #c.Lang = "en"
    c.Count = True
    c.Store_json = True
    #c.Store_csv =
    #c.Output = "./MFA_China.txt"
    #c.Since = '2019-9-28'
    #c.Until = "2021-10-15"
    #c.Location = True
    #c.Limit = 200
    #c.Profile_full = True
    #c.Media = True
    #c.Retweets = True
    #c.Filter_retweets = True

    c.Custom["tweet"] = ["id", "date", "username", "name", "tweet", "urls", "replies_count", "retweets_count", "mentions", "likes_count", "hashtags", "cashtags", "retweet", "quote_url", "retweet_date", "user_rt_id"]
    # "id", "date", "username", "name", "tweet", "replies_count", "retweets_count", "mentions", "likes_count", "hashtags", "cashtags", "retweet", "quote_url", "retweet_date", "user_rt_id"

    #if ElaSearch:
    #    c.Elasticsearch = "http://localhost:9200"

    #print(c)
    #for user in User_list:
    c.Username = user
    print('trying to get ', c.Username)
    #c.Search = kw
    #print(c.Retweets)
    print(c)
    c.Output = './{}.json'.format(user)
    twint.run.Search(c)

    print("done with ", c.Username)

    print("tweets all done")


def get_mention_users():
    user_list = []
    with open('MFA_China.txt', 'r', encoding='utf-8') as f:
        for jsonstr in f.readlines():
            jsonstr = json.loads(jsonstr)
            for user in jsonstr['mentions']:
                user_name = user['screen_name']
                if user_name not in user_list:
                    user_list.append(user_name)
    #print(sorted(user_list))
    return sorted(user_list)


def find_missing():
    file_name = os.listdir('./lv1Related')
    sp_file = []
    for f in file_name:
        sp_file.append(f.split('.')[0])
    print(sp_file)

    missing = []
    user_list = get_mention_users()
    for user in user_list:
        print(user)
        if user not in sp_file:
            missing.append(user)

    print(missing)
    return missing


'''userList = get_mention_users()
#print(len(userList))
#print(userList)
print(len(userList))
for user in userList:
    fetch_tweet(user)
'''

# fetch_tweet('zlj517')
'''c = twint.Config()
c.Username = 'RNG'
twint.run.Lookup(c) '''

#fetch_tweet('zlj517')