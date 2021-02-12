import pandas as pd
import snscrape.modules.twitter as sntwitter
import itertools

stocks_acronym = ['PANW','AMT','ADI','TMUS','AAPL','ERIC','QCOM','SQ','OKTA','COUP','MELI',
                    'PYPL','BABA', 'SHOP','NVDA','CRM','AMZN','MSFT','GOOGL']

stocks_name = ['Palo Alto Networks','American Tower','Analog Devices','T-Mobile','Apple','Ericsson','Qualcomm',
                'Square','Okta','Coupa Software','MercadoLibre','Paypal','Alibaba','Shopify','NVIDIA',
                'Salesforce','Amazon','Microsoft','Google']

# Setting variables to be used below
maxTweets = 500

# Creating list to append tweet data to
tweets_list = []

# Using TwitterSearchScraper to scrape data and append tweets to list
for i,tweet in enumerate(sntwitter.TwitterSearchScraper('AMT since:2020-07-01 until:2020-09-05').get_items()):
    if i>maxTweets:
        break
    #tweets_list.append([tweet.date, tweet.id, tweet.content, tweet.replyCount, tweet.retweetCount, tweet.likeCount, tweet.quoteCount])
    tweets_list.append([tweet.date, tweet.id, tweet.content, tweet.likeCount])

# Creating a dataframe from the tweets list above
tweets_df = pd.DataFrame(tweets_list, columns=['Datetime', 'Tweet Id', 'Content', ])

# Display first 5 entries from dataframe
tweets_df.head()

# Export dataframe into a CSV
tweets_df.to_csv('text-query-tweets.csv', sep=',', index=False)







from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download("vader_lexicon")
sentimentAnalyser = SentimentIntensityAnalyzer()
tweets_df["compound"] = [sentimentAnalyser.polarity_scores(v)['compound'] for v in tweets_df["Content"]]
tweets_df["negative"] = [sentimentAnalyser.polarity_scores(v)['neg'] for v in tweets_df["Content"]]
tweets_df["positive"] = [sentimentAnalyser.polarity_scores(v)['pos'] for v in tweets_df["Content"]]
tweets_df["neutral"] = [sentimentAnalyser.polarity_scores(v)['neu'] for v in tweets_df["Content"]]

tweets_df = tweets_df.sort_values(by="Datetime")

tweets_df['weekly_average'] = tweets_df['compound'].rolling(7, win_type='triang').sum()
tweets_df['monthly_average'] = tweets_df['compound'].rolling(30, win_type='triang').sum()

print(tweets_df)