from psaw import PushshiftAPI
import datetime as dt
import pandas as pd
import praw
import sys
import os
import numpy as np
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download("vader_lexicon")

def getReddit_data():
    '''
    Collects two years(from present to two years ago) of reddit data from the PSAW API relating
    to specific stocks. Then creates a csv for each stock containing the data.

    Data collected:
        Top 5 reddit posts per day
        Top 5 reddit comments per day
    
    Raw Data is stored in Data/Reddit_data/reddit_Rawdata
    '''
    # Get file paths and directories
    red_scrapper_dir=os.path.abspath(os.curdir)#current working Directory
    repo_Dir = os.path.dirname(os.path.dirname(os.path.dirname(red_scrapper_dir)))
    data_Dir = os.path.join(repo_Dir,"Data")
    red_Dir = os.path.join(data_Dir,"Reddit_data")
    raw_dataDir = os.path.join(red_Dir,"reddit_Rawdata")

    sub_Dir = os.path.join(raw_dataDir,"submission_Rawdata")
    com_Dir = os.path.join(raw_dataDir,"comments_Rawdata")

    os.chdir(red_Dir)
    if not os.path.isdir(raw_dataDir):
        # directory does not exist so create directory
        os.mkdir(raw_dataDir)
    os.chdir(raw_dataDir)
    if not os.path.isdir(sub_Dir):
        # directory does not exist so create directory
        os.mkdir(sub_Dir)
    if not os.path.isdir(com_Dir):
        # directory does not exist so create directory
        os.mkdir(com_Dir)

    # change directory just to be within main raw reddit data directory
    os.chdir(raw_dataDir)

    sentimentAnalyser = SentimentIntensityAnalyzer()
    now = dt.datetime.now()

    stocks_acronym = ['PANW','AMT','ADI','TMUS','AAPL','ERIC','QCOM','SQ','OKTA','COUP','MELI',
                        'PYPL','BABA', 'SHOP','NVDA','CRM','AMZN','MSFT','GOOGL']

    stocks_name = ['Palo Alto Networks','American Tower','Analog Devices','T-Mobile','Apple','Ericsson','Qualcomm',
                    'Square','Okta','Coupa Software','MercadoLibre','Paypal','Alibaba','Shopify','NVIDIA',
                    'Salesforce','Amazon','Microsoft','Google']

    api = PushshiftAPI()

    temp_df = pd.DataFrame()
    df1 = pd.DataFrame()    #empty dataframe
    df2 = pd.DataFrame()    #empty dataframe
    empty_dataframe = False
    for stock in stocks_acronym:
        for cnt in range(2*365+1):
            date_temp = now - dt.timedelta(days=(2*365+1)-cnt)
            date_temp2 = now - dt.timedelta(days=(2*365+1)-cnt-1)
            date_iter = int(dt.datetime(date_temp.year,date_temp.month,date_temp.day).timestamp())
            date_iter2 = int(dt.datetime(date_temp2.year,date_temp2.month,date_temp2.day).timestamp())

            # Get submissions
            data_sub = list(api.search_submissions(after=date_iter,
                                        before=date_iter2,
                                        q=stock,
                                        filter=['id','title', 'score','selftext','num_comments','last_updated'],
                                        limit=5, sort="desc", sort_type="score"))
            
            try:
                df_sub = pd.DataFrame(data_sub)
            except:
                #Error: ValueError: 7 columns passed, passed data had 8 columns
                print(f"Stock: {stock}, after: {date_temp}, before: {date_temp2}")
                print(data_sub)
                if input("enter 'c' to continue(anything else to exit program): ")=='c':
                    continue
                else:
                    sys.exit()

            try:
                df_sub['created_utc'] = df_sub['created_utc'].apply(lambda x: dt.datetime.fromtimestamp(x))
                df_sub['created'] = df_sub['created'].apply(lambda x: dt.datetime.fromtimestamp(x))
            except:
                #print("couldn't convert date")
                not_needed_val = 1
            
            # vertical stack the dataframes
            if df1.empty:
                df1 = df_sub
            else:
                df1 = pd.concat([df1,df_sub],axis=0)

            # Get comments
            data_com = list(api.search_comments(after=date_iter,
                                before=date_iter2,
                                q=stock,
                                filter=['body'],
                                limit=5, sort="desc", sort_type="score"))

            df_com = pd.DataFrame(data_com)
            try:
                df_com['created_utc'] = df_com['created_utc'].apply(lambda x: dt.datetime.fromtimestamp(x))
                df_com['created'] = df_com['created'].apply(lambda x: dt.datetime.fromtimestamp(x))
            except:
                #print("couldn't convert date")
                not_needed_val = 1

            # vertical stack the dataframes
            if df2.empty:
                df2 = df_com
            else:
                df2 = pd.concat([df2,df_com],axis=0)
            
            #reset
            df_sub = pd.DataFrame()
            df_com = pd.DataFrame()
            temp_df = pd.DataFrame()
            empty_dataframe = False
            


        # Get Sentiment values for every post
        for index,row in df1.iterrows():
            try:
                row['combined_text']=row['title'] + row['selftext']
            except:
                row['combined_text'] = row['title']
        if ('title' in df1.columns):
            try:
                df1["compound"] = [sentimentAnalyser.polarity_scores(str(v))['compound'] for v in df1["combined_text"]]
                df1["negative"] = [sentimentAnalyser.polarity_scores(str(v))['neg'] for v in df1["combined_text"]]
                df1["positive"] = [sentimentAnalyser.polarity_scores(str(v))['pos'] for v in df1["combined_text"]]
                df1["neutral"] = [sentimentAnalyser.polarity_scores(str(v))['neu'] for v in df1["combined_text"]]
            except:
                df1["compound"] = [sentimentAnalyser.polarity_scores(str(v))['compound'] for v in df1["title"]]
                df1["negative"] = [sentimentAnalyser.polarity_scores(str(v))['neg'] for v in df1["title"]]
                df1["positive"] = [sentimentAnalyser.polarity_scores(str(v))['pos'] for v in df1["title"]]
                df1["neutral"] = [sentimentAnalyser.polarity_scores(str(v))['neu'] for v in df1["title"]]

        df2["compound"] = [sentimentAnalyser.polarity_scores(v)['compound'] for v in df2["body"]]
        df2["negative"] = [sentimentAnalyser.polarity_scores(v)['neg'] for v in df2["body"]]
        df2["positive"] = [sentimentAnalyser.polarity_scores(v)['pos'] for v in df2["body"]]
        df2["neutral"] = [sentimentAnalyser.polarity_scores(v)['neu'] for v in df2["body"]]

        os.chdir(sub_Dir)
        df1.to_csv(stock+'_sub'+'.csv',index=False)
        os.chdir(com_Dir)
        df2.to_csv(stock+'_com'+'.csv',index=False)
        os.chdir(raw_dataDir)

        #reset
        df1 = pd.DataFrame()    #empty dataframe
        df2 = pd.DataFrame()    #empty dataframe
        df_sub = pd.DataFrame()
        df_com = pd.DataFrame()

if __name__ == "__main__":
    getReddit_data()