import pandas as pd
import snscrape.modules.twitter as sntwitter
import itertools
import datetime as dt

now = dt.datetime.now()
prev = now - dt.timedelta(days=2*365+1)

# stocks_acronym = ['PANW','AMT','ADI','TMUS','AAPL','ERIC','QCOM','SQ','OKTA','COUP','MELI',
#                     'PYPL','BABA', 'SHOP','NVDA','CRM','AMZN','MSFT','GOOGL']
stocks_acronym = ['ADI','TMUS','AAPL','ERIC','QCOM','SQ','OKTA','COUP','MELI',
                    'PYPL','BABA', 'SHOP','NVDA','CRM','AMZN','MSFT','GOOGL']

stocks_name = ['Palo Alto Networks','American Tower','Analog Devices','T-Mobile','Apple','Ericsson','Qualcomm',
                'Square','Okta','Coupa Software','MercadoLibre','Paypal','Alibaba','Shopify','NVIDIA',
                'Salesforce','Amazon','Microsoft','Google']

# # Setting variables to be used below
# maxTweets = 500

# Creating list to append tweet data to
tweets_list = []

# # Using TwitterSearchScraper to scrape data and append tweets to list
# for i,tweet in enumerate(sntwitter.TwitterSearchScraper('AMT since:2020-07-01 until:2020-09-05').get_items()):
#     if i>maxTweets:
#         break
#     #tweets_list.append([tweet.date, tweet.id, tweet.content, tweet.replyCount, tweet.retweetCount, tweet.likeCount, tweet.quoteCount])
#     tweets_list.append([tweet.date, tweet.id, tweet.content, tweet.likeCount])

# # Creating a dataframe from the tweets list above
# tweets_df = pd.DataFrame(tweets_list, columns=['Datetime', 'Tweet Id', 'Content', ])

# # Display first 5 entries from dataframe
# tweets_df.head()

# # Export dataframe into a CSV
# tweets_df.to_csv('text-query-tweets.csv', sep=',', index=False)

# from nltk.sentiment.vader import SentimentIntensityAnalyzer
# import nltk
# nltk.download("vader_lexicon")
# sentimentAnalyser = SentimentIntensityAnalyzer()
# tweets_df["compound"] = [sentimentAnalyser.polarity_scores(v)['compound'] for v in tweets_df["Content"]]
# tweets_df["negative"] = [sentimentAnalyser.polarity_scores(v)['neg'] for v in tweets_df["Content"]]
# tweets_df["positive"] = [sentimentAnalyser.polarity_scores(v)['pos'] for v in tweets_df["Content"]]
# tweets_df["neutral"] = [sentimentAnalyser.polarity_scores(v)['neu'] for v in tweets_df["Content"]]

# tweets_df = tweets_df.sort_values(by="Datetime")

# tweets_df['weekly_average'] = tweets_df['compound'].rolling(7, win_type='triang').sum()
# tweets_df['monthly_average'] = tweets_df['compound'].rolling(30, win_type='triang').sum()

# print(tweets_df)



from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download("vader_lexicon")

sentimentAnalyser = SentimentIntensityAnalyzer()            # Does this need to be re-initialized?????????? after every iteration
# Fix date values for input to twitter search
# now date
if len(str(prev.month)):
    pre_month_val = '0'+str(prev.month)
else:
    pre_month_val = str(prev.month)

if len(str(prev.day)):
    pre_day_val = '0'+str(prev.day)
else:
    pre_day_val = str(prev.day)

# prev date
if len(str(now.month)):
    now_month_val = '0'+str(now.month)
else:
    now_month_val = str(now.month)

if len(str(now.day)):
    now_day_val = '0'+str(now.day)
else:
    now_day_val = str(now.day)

since_val = 'since:' + str(prev.year) + '-' + pre_month_val + '-' + pre_day_val
until_val = 'until:' + str(now.year) + '-' + now_month_val + '-' + now_day_val
# search for tweets
for stock in stocks_acronym:
    search_str = stock + ' ' + since_val + ' ' + until_val
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper(search_str).get_items()):
        try:
            tweets_list.append([tweet.date, tweet.id, tweet.content])
        except:
            continue

    tweets_df = pd.DataFrame(tweets_list, columns=['Datetime', 'Tweet Id', 'Content', ])

    tweets_df["compound"] = [sentimentAnalyser.polarity_scores(v)['compound'] for v in tweets_df["Content"]]
    tweets_df["negative"] = [sentimentAnalyser.polarity_scores(v)['neg'] for v in tweets_df["Content"]]
    tweets_df["positive"] = [sentimentAnalyser.polarity_scores(v)['pos'] for v in tweets_df["Content"]]
    tweets_df["neutral"] = [sentimentAnalyser.polarity_scores(v)['neu'] for v in tweets_df["Content"]]

    tweets_df = tweets_df.sort_values(by="Datetime")

    tweets_df['weekly_average'] = tweets_df['compound'].rolling(7, win_type='triang').sum()
    tweets_df['monthly_average'] = tweets_df['compound'].rolling(30, win_type='triang').sum()

    tweets_df.to_csv(stock+'.csv',index=False)