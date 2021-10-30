import twint
import asyncio
import snscrape.modules.twitter as snscrapetwt
'''
tweet_list = []
for i, tweet in enumerate(snscrapetwt.TwitterSearchScraper('from:zlj517').get_items()):
    if i > 2000:
        break
    tweet_list.append(tweet)

for tt in tweet_list:
    print(type(tt))'''

"https://api.twitter.com/2/timeline/profile/${uid}.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_composer_source=true&include_ext_alt_text=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&send_error_codes=true&simple_quoted_tweets=true&ext=mediaStats%2CcameraMoment&count=${count}&cursor=${cursor}"
