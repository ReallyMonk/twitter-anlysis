import json

filepath = "./MFA_chian.json"
outfile = "./MFA_ChinaRes_pb"
ignore_words = ["&amp;"]
ignore_sym = "🔗➡️👏👍👂👀👇🌆🧐😍"


def extract_txt(fpath, opath, label=False):
    if not label:
        opath = opath + '.txt'
    else:
        opath = opath + '.json'
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        for jsonstr in f.readlines():
            # pick info from json file
            jsonstr = json.loads(jsonstr)
            tweet = jsonstr["tweet"].split("http")[0]
            label = jsonstr["hashtags"] if jsonstr['hashtags'] != [] else ['rest']

            # throw the meaning less words or symbols
            for ig_w in ignore_words:
                if ig_w in tweet:
                    tweet = tweet.replace(ig_w, '&')
            for ig_w in ignore_sym:
                if ig_w in tweet:
                    tweet = tweet.replace(ig_w, '')

            # ignore tweets without a word
            if tweet == " ":
                continue

            # write new info
            # to txt file if none label
            # to json file if label
            if not label:
                with open(opath, 'a', encoding='utf-8') as ofile:
                    ofile.write(tweet + '\n')
            else:
                twtjson = {'tweet': tweet, 'label': label}

                with open(opath, 'a') as ofile:
                    json.dump(twtjson, ofile)
                    ofile.write('\n')


extract_txt(filepath, outfile, True)
