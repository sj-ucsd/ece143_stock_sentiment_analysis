import pandas as pd
import snscrape.modules.twitter as sntwitter
import itertools
import datetime as dt
import os

def getTwitter_data():
    # Get file paths and directories
    twit_scrapper_dir=os.path.abspath(os.curdir)#current working Directory
    repo_Dir = os.path.dirname(os.path.dirname(os.path.dirname(twit_scrapper_dir)))
    data_Dir = os.path.join(repo_Dir,"Data")
    twit_Dir = os.path.join(data_Dir,"Twitter_data")

    raw_dataDir = os.path.join(twit_Dir,"twitter_RawData")

    if not os.path.isdir(raw_dataDir):
        # directory does not exist so create directory
        os.mkdir(raw_dataDir)
    os.chdir(raw_dataDir)

    now = dt.datetime.now()
    prev = now - dt.timedelta(days=2*365+1)

    stocks_acronym = ['PANW','AMT','ADI','TMUS','AAPL','ERIC','QCOM','SQ','OKTA','COUP','MELI',
                        'PYPL','BABA', 'SHOP','NVDA','CRM','AMZN','MSFT','GOOGL']

    stocks_name = ['Palo Alto Networks','American Tower','Analog Devices','T-Mobile','Apple','Ericsson','Qualcomm',
                    'Square','Okta','Coupa Software','MercadoLibre','Paypal','Alibaba','Shopify','NVIDIA',
                    'Salesforce','Amazon','Microsoft','Google']

    # # Setting variables to be used below
    # maxTweets = 500

    # Creating list to append tweet data to
    tweets_list = []

    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    import nltk
    nltk.download("vader_lexicon")

    sentimentAnalyser = SentimentIntensityAnalyzer()   
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

        tweets_df.to_csv(stock+'.csv',index=False)

if __name__ == "__main__":
    getTwitter_data()