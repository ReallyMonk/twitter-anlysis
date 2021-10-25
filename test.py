from twitter_scraper import get_tweets
import twint
import asyncio
import snscrape.modules.twitter as snscrapetwt

tweet_list = []
for i, tweet in enumerate(snscrapetwt.TwitterSearchScraper('COVID Vaccine since:2021-01-01 until:2021-05-31').get_items()):
    if i > 100:
        break
    tweet_list.append(tweet)

for tt in tweet_list:
    print(type(tt))