'''
Run this script from terminal
'''
import pandas as pd
import snscrape.modules.twitter as sntwitter
import itertools

# Setting variables to be used below
#maxTweets = 50

# Creating list to append tweet data to
tweets_list = []

# Using TwitterSearchScraper to scrape data and append tweets to list
for i,tweet in enumerate(sntwitter.TwitterSearchScraper('AMT since:2020-03-01 until:2020-09-05').get_items()):
    # if i>maxTweets:
    #     break
    #tweets_list.append([tweet.date, tweet.id, tweet.content, tweet.replyCount, tweet.retweetCount, tweet.likeCount, tweet.quoteCount])
    tweets_list.append([tweet.date, tweet.id, tweet.content])

# Creating a dataframe from the tweets list above
tweets_df = pd.DataFrame(tweets_list, columns=['Datetime', 'Tweet Id', 'Content', ])

# Display first 5 entries from dataframe
tweets_df.head()

# Export dataframe into a CSV
tweets_df.to_csv('text-query-tweets.csv', sep=',', index=False)

