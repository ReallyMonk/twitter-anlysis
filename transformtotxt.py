import json


filepath = "./Spokesperson.json"
outfile = "./Spokesperson.txt"
ignore_words = ["&amp;"]
ignore_sym = "🔗➡️👏👍👂👀👇🌆🧐😍"

def extract_txt(fpath, opath):
    with open(fpath, 'r', encoding='utf-8',errors='ignore') as f:
        for jsonstr in f.readlines():
            jsonstr = json.loads(jsonstr)
            tweet = jsonstr["tweet"].split("http")[0] + '\n'

            print(tweet)

            for ig_w in ignore_words:
                #print(ig_w)
                if ig_w in tweet:
                    tweet = tweet.replace(ig_w, '&')
            
            for ig_w in ignore_sym:
                #print(ig_w)
                if ig_w in tweet:
                    tweet = tweet.replace(ig_w, '')

            #print(tweet)
            ofile = open(opath, 'a', encoding='utf-8')
            ofile.write(tweet)
            ofile.close()
            

            #print(jsonstr["tweet"].split("http")[0])


extract_txt(filepath, outfile)

