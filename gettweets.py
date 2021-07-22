import twint
'''
ERROR: User been defined nonetype
solved by executing following
pip3 install --upgrade -e git+https://github.com/twintproject/twint.git@origin/master#egg=twint
'''



userList = ["MFA_China"]#,"CHN_UN_NY","zlj517","SpokespersonCHN","ChinaEUMission","China2ASEAN","AmbCuiTiankai","chianscio"]#,"gZclW78FYo7XYMO","China2ASEAN", "MFA_China2", "libijian2", "AmbCuiTiankai", "ChineseEmbinUS"]
mediaList = ["CGTNOfficial", "PDChina", "XHNews"]
kwList = [""]

def fetch_tweet(User_list, keywords_list, ElaSearch=False):
    c = twint.Config()
    #c.Lang = "en"
    c.Count =True
    c.Store_json = True
    #c.Store_csv = 
    c.Output = "./Spokesperson.json"
    #c.Since = '2020-06-01'
    #c.Limit = 100
    #c.Retweets = True
    #c.Filter_retweets = True

    c.Custom["tweet"] = ["id","date","username","name","tweet","replies_count","retweets_count","mentions","likes_count","hashtags","retweet"]

    if ElaSearch:
        c.Elasticsearch = "http://localhost:9200"


    for user in User_list:
        for kw in keywords_list:
            c.Username = user
            c.Search = kw
            #print(c.Retweets)
            twint.run.Search(c)
        
        print("done with ", c.Username)
    
    print("tweets all done")


#def seperate_tweets():

#fetch_tweet(mediaList, kwList)
fetch_tweet(userList, kwList, True)