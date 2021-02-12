from psaw import PushshiftAPI
import datetime as dt
import pandas as pd
import praw

'''
Palo Alto Networks
American Tower
Analog Devices
T-Mobile
Apple
Ericsson
Qualcomm

E Commerce Stocks
Square
Okta
Coupa Software
MercadoLibre
Paypal
Alibaba
Shopify

AI Space
NVIDIA
Salesforce
Amazon
Microsoft
Google
'''
stocks_acronym = ['PANW','AMT','ADI','TMUS','AAPL','ERIC','QCOM','SQ','OKTA','COUP','MELI',
                    'PYPL','BABA', 'SHOP','NVDA','CRM','AMZN','MSFT','GOOGL']

stocks_name = ['Palo Alto Networks','American Tower','Analog Devices','T-Mobile','Apple','Ericsson','Qualcomm',
                'Square','Okta','Coupa Software','MercadoLibre','Paypal','Alibaba','Shopify','NVIDIA',
                'Salesforce','Amazon','Microsoft','Google']

api = PushshiftAPI()

start_epoch=int(dt.datetime(2019, 1, 2).timestamp())

end_epoch = int(dt.datetime(2020, 1,10).timestamp())

# data = list(api.search_submissions(after=start_epoch,
#                             before=end_epoch,
#                             q="qualcomm",
#                             subreddit='wallstreetbets',
#                             filter=['title', 'score', 'num_comments','last_updated'],
#                             limit=2, sort="desc", sort_type="score"))

data = list(api.search_submissions(after=start_epoch,
                            before=end_epoch,
                            q="qualcomm",
                            filter=['id','url','title', 'score', 'subreddit','selftext','text','num_comments','last_updated'],
                            limit=10, sort="desc", sort_type="score"))

df = pd.DataFrame(data)
print(df)
df.to_csv('stockEX.csv',index=False)

# start_epoch=int(dt.datetime(2019, 1, 3).timestamp())
# data = list(api.search_comments(after=start_epoch,
#                             q="qualcomm",
#                             subreddit='wallstreetbets',
#                             filter=['body'],
#                             limit=10, sort="desc", sort_type="score"))







from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download("vader_lexicon")
sentimentAnalyser = SentimentIntensityAnalyzer()
df["compound"] = [sentimentAnalyser.polarity_scores(v)['compound'] for v in df["title"]]
df["negative"] = [sentimentAnalyser.polarity_scores(v)['neg'] for v in df["title"]]
df["positive"] = [sentimentAnalyser.polarity_scores(v)['pos'] for v in df["title"]]
df["neutral"] = [sentimentAnalyser.polarity_scores(v)['neu'] for v in df["title"]]

df = df.sort_values(by="created")

df['weekly_average'] = df['compound'].rolling(7, win_type='triang').sum()
df['monthly_average'] = df['compound'].rolling(30, win_type='triang').sum()

print(df)