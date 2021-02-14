'''
This file was designed to be ran from within the reddit_data folder
    It is also expected for this folder to contain no extra directories

Any directories in this directory may be overwritten if this script is ran

This script should work on Mac. Ask Nick first before running this script
-Nick Munoz
'''
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

# Get file paths and directories
main_WorkingDir=os.path.abspath(os.curdir)#current working Directory
avg_Dir = os.path.join(main_WorkingDir,"Daily_avg")
data_Dir = os.path.join(main_WorkingDir,"redditStock_data")
sub_Dir = os.path.join(data_Dir,"submission_data")
com_Dir = os.path.join(data_Dir,"comments_data")
# os.mkdir(avg_Dir)
# os.mkdir(data_Dir)
# os.chdir(data_Dir)
# os.mkdir(sub_Dir)
# os.mkdir(com_Dir)
# os.chdir(main_WorkingDir)
# print(os.path.abspath(os.curdir))
# sys.exit()

sentimentAnalyser = SentimentIntensityAnalyzer()
now = dt.datetime.now()
#prev = now - dt.timedelta(days=2*365+1)

# stocks_acronym = ['PANW','AMT','ADI','TMUS','AAPL','ERIC','QCOM','SQ','OKTA','COUP','MELI',
#                     'PYPL','BABA', 'SHOP','NVDA','CRM','AMZN','MSFT','GOOGL']

stocks_acronym = ['PYPL','BABA', 'SHOP','NVDA','CRM','AMZN','MSFT','GOOGL']

stocks_name = ['Palo Alto Networks','American Tower','Analog Devices','T-Mobile','Apple','Ericsson','Qualcomm',
                'Square','Okta','Coupa Software','MercadoLibre','Paypal','Alibaba','Shopify','NVIDIA',
                'Salesforce','Amazon','Microsoft','Google']

#investing,stocks,wallstreetbets
api = PushshiftAPI()

#start_epoch=int(dt.datetime(2019, 1, 2).timestamp())
#start_epoch = int(dt.datetime(prev.year,prev.month,prev.day).timestamp())
#end_epoch = int(dt.datetime(2020, 1,10).timestamp())
#end_epoch = int(dt.datetime(now.year,now.month,now.day).timestamp())

df_sentiment = pd.DataFrame()   #empty dataframe
temp_df = pd.DataFrame()
df1 = pd.DataFrame()    #empty dataframe
df2 = pd.DataFrame()    #empty dataframe
empty_dataframe = False
for stock in stocks_acronym:
    for cnt in range(2*365+1):
        #This may be possibly two days of data because of the logic designed below
        # Need to find how to do a single day specifically
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
        
        df_sub = pd.DataFrame(data_sub)
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

        # Get sentiment
        for index,row in df_sub.iterrows():
            try:
                row['combined_text']=row['title'] + row['selftext']
            except:
                row['combined_text'] = row['title']
        if ('title' in df_sub.columns):
            # df_sub["combined_text"]= df_sub['title'] + df_sub['selftext']
            try:
                df_sub["compound"] = [sentimentAnalyser.polarity_scores(str(v))['compound'] for v in df_sub["combined_text"]]
                df_sub["negative"] = [sentimentAnalyser.polarity_scores(str(v))['neg'] for v in df_sub["combined_text"]]
                df_sub["positive"] = [sentimentAnalyser.polarity_scores(str(v))['pos'] for v in df_sub["combined_text"]]
                df_sub["neutral"] = [sentimentAnalyser.polarity_scores(str(v))['neu'] for v in df_sub["combined_text"]]
            except:
                df_sub["compound"] = [sentimentAnalyser.polarity_scores(str(v))['compound'] for v in df_sub["title"]]
                df_sub["negative"] = [sentimentAnalyser.polarity_scores(str(v))['neg'] for v in df_sub["title"]]
                df_sub["positive"] = [sentimentAnalyser.polarity_scores(str(v))['pos'] for v in df_sub["title"]]
                df_sub["neutral"] = [sentimentAnalyser.polarity_scores(str(v))['neu'] for v in df_sub["title"]]
        # elif ('title' in df_sub.columns):
        #     df_sub["combined_text"]= df_sub['title']
        #     df_sub["compound"] = [sentimentAnalyser.polarity_scores(v)['compound'] for v in df_sub["combined_text"]]
        #     df_sub["negative"] = [sentimentAnalyser.polarity_scores(v)['neg'] for v in df_sub["combined_text"]]
        #     df_sub["positive"] = [sentimentAnalyser.polarity_scores(v)['pos'] for v in df_sub["combined_text"]]
        #     df_sub["neutral"] = [sentimentAnalyser.polarity_scores(v)['neu'] for v in df_sub["combined_text"]]
            
        # for index,row in df_sub.iterrows():
        #     if 'selftext' in df_sub.columns or 'title' in df_sub.columns:
        #         try:
        #             row["compound"] = sentimentAnalyser.polarity_scores(row['selftext'])['compound']
        #             row["negative"] = sentimentAnalyser.polarity_scores(row['selftext'])['neg']
        #             row["positive"] = sentimentAnalyser.polarity_scores(row['selftext'])['pos']
        #             row["neutral"] = sentimentAnalyser.polarity_scores(row['selftext'])['neu']
        #         except:
        #             row["compound"] = sentimentAnalyser.polarity_scores(row['title'])['compound']
        #             row["negative"] = sentimentAnalyser.polarity_scores(row['title'])['neg']
        #             row["positive"] = sentimentAnalyser.polarity_scores(row['title'])['pos']
        #             row["neutral"] = sentimentAnalyser.polarity_scores(row['title'])['neu']
        #     # if (row['selftext'] == "") or (pd.isnull(row['selftext'])):
        #     #     # this reddit post has no body text so use title
        #     #     row["compound"] = sentimentAnalyser.polarity_scores(row['title'])['compound']
        #     #     row["negative"] = sentimentAnalyser.polarity_scores(row['title'])['neg']
        #     #     row["positive"] = sentimentAnalyser.polarity_scores(row['title'])['pos']
        #     #     row["neutral"] = sentimentAnalyser.polarity_scores(row['title'])['neu']
        #     # else:
        #     #     row["compound"] = sentimentAnalyser.polarity_scores(row['selftext'])['compound']
        #     #     row["negative"] = sentimentAnalyser.polarity_scores(row['selftext'])['neg']
        #     #     row["positive"] = sentimentAnalyser.polarity_scores(row['selftext'])['pos']
        #     #     row["neutral"] = sentimentAnalyser.polarity_scores(row['selftext'])['neu']
        
        #sys.exit()
        
        if not df_com.empty and ('body' in df_sub.columns):
            df_com["compound"] = [sentimentAnalyser.polarity_scores(v)['compound'] for v in df_com["body"]]
            df_com["negative"] = [sentimentAnalyser.polarity_scores(v)['neg'] for v in df_com["body"]]
            df_com["positive"] = [sentimentAnalyser.polarity_scores(v)['pos'] for v in df_com["body"]]
            df_com["neutral"] = [sentimentAnalyser.polarity_scores(v)['neu'] for v in df_com["body"]]

        #Get daily avg sentiment
        if ('compound' not in df_sub.columns) and ('compound' not in df_com.columns):
            #No reddit data was collected for this day
            empty_dataframe = True
        elif df_sub.empty and ('compound' in df_com.columns):
            temp_df['Date'] = df_com['created_utc']
            temp_df['avg_compound'] = df_com['compound']
            temp_df['avg_negative'] = df_com['negative']
            temp_df['avg_positive'] = df_com['positive']
            temp_df['avg_neutral'] = df_com['neutral']
        elif df_com.empty and ('compound' in df_sub.columns):
            temp_df['Date'] = df_sub['created_utc']
            temp_df['avg_compound'] = df_sub['compound']
            temp_df['avg_negative'] = df_sub['negative']
            temp_df['avg_positive'] = df_sub['positive']
            temp_df['avg_neutral'] = df_sub['neutral']
        elif ('compound' in df_sub.columns) and ('compound' in df_com.columns):
            temp_df['Date'] = df_sub['created_utc']     #either dataframe could have been used for this
            temp_df['avg_compound'] = (df_sub['compound'].sum() + df_com['compound'].sum())/(df_sub['compound'].count() + df_com['compound'].count())
            temp_df['avg_negative'] = (df_sub['negative'].sum() + df_com['negative'].sum())/(df_sub['negative'].count() + df_com['negative'].count())
            temp_df['avg_positive'] = (df_sub['positive'].sum() + df_com['positive'].sum())/(df_sub['positive'].count() + df_com['positive'].count())
            temp_df['avg_neutral'] = (df_sub['neutral'].sum() + df_com['neutral'].sum())/(df_sub['neutral'].count() + df_com['neutral'].count())

        # vertical stack the dataframes
        if not empty_dataframe:     #only do this if both dataframe is not empty => New data was collected
            if df_sentiment.empty:
                df_sentiment = temp_df
            else:
                df_sentiment = pd.concat([df_sentiment,temp_df],axis=0)
        
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
        # df1["combined_text"]= df1['title'] + df1['selftext'] 
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
# elif ('title' in df1.columns):
    #     df1["combined_text"]= df1['title']
    #     df1["compound"] = [sentimentAnalyser.polarity_scores(v)['compound'] for v in df1["combined_text"]]
    #     df1["negative"] = [sentimentAnalyser.polarity_scores(v)['neg'] for v in df1["combined_text"]]
    #     df1["positive"] = [sentimentAnalyser.polarity_scores(v)['pos'] for v in df1["combined_text"]]
    #     df1["neutral"] = [sentimentAnalyser.polarity_scores(v)['neu'] for v in df1["combined_text"]]
    # # Have someone verify logic
    # for index,row in df1.iterrows():
    #     try:
    #         row["compound"] = sentimentAnalyser.polarity_scores(row['selftext'])['compound']
    #         row["negative"] = sentimentAnalyser.polarity_scores(row['selftext'])['neg']
    #         row["positive"] = sentimentAnalyser.polarity_scores(row['selftext'])['pos']
    #         row["neutral"] = sentimentAnalyser.polarity_scores(row['selftext'])['neu']
    #     except:
    #         row["compound"] = sentimentAnalyser.polarity_scores(row['title'])['compound']
    #         row["negative"] = sentimentAnalyser.polarity_scores(row['title'])['neg']
    #         row["positive"] = sentimentAnalyser.polarity_scores(row['title'])['pos']
    #         row["neutral"] = sentimentAnalyser.polarity_scores(row['title'])['neu']
    #     # if (row['selftext'] == "") or (pd.isnull(row['selftext'])):
    #     #     # this reddit post has no body text so use title
    #     #     row["compound"] = sentimentAnalyser.polarity_scores(row['title'])['compound']
    #     #     row["negative"] = sentimentAnalyser.polarity_scores(row['title'])['neg']
    #     #     row["positive"] = sentimentAnalyser.polarity_scores(row['title'])['pos']
    #     #     row["neutral"] = sentimentAnalyser.polarity_scores(row['title'])['neu']
    #     # else:
    #     #     row["compound"] = sentimentAnalyser.polarity_scores(row['selftext'])['compound']
    #     #     row["negative"] = sentimentAnalyser.polarity_scores(row['selftext'])['neg']
    #     #     row["positive"] = sentimentAnalyser.polarity_scores(row['selftext'])['pos']
    #     #     row["neutral"] = sentimentAnalyser.polarity_scores(row['selftext'])['neu']
    # print(df1)
    df1['weekly_average'] = df1['compound'].rolling(7, win_type='triang').sum()
    df1['monthly_average'] = df1['compound'].rolling(30, win_type='triang').sum()

    df2["compound"] = [sentimentAnalyser.polarity_scores(v)['compound'] for v in df2["body"]]
    df2["negative"] = [sentimentAnalyser.polarity_scores(v)['neg'] for v in df2["body"]]
    df2["positive"] = [sentimentAnalyser.polarity_scores(v)['pos'] for v in df2["body"]]
    df2["neutral"] = [sentimentAnalyser.polarity_scores(v)['neu'] for v in df2["body"]]

    df2['weekly_average'] = df2['compound'].rolling(7, win_type='triang').sum()
    df2['monthly_average'] = df2['compound'].rolling(30, win_type='triang').sum()

    os.chdir(sub_Dir)
    df1.to_csv(stock+'_sub'+'.csv',index=False)
    os.chdir(com_Dir)
    df2.to_csv(stock+'_com'+'.csv',index=False)
    os.chdir(avg_Dir)
    df_sentiment.to_csv(stock+'_daily_avg.csv',index = False)
    os.chdir(main_WorkingDir)

    #reset
    df_sentiment = pd.DataFrame()   #empty dataframe
    df1 = pd.DataFrame()    #empty dataframe
    df2 = pd.DataFrame()    #empty dataframe
    df_sub = pd.DataFrame()
    df_com = pd.DataFrame()




# df['weekly_average'] = df['compound'].rolling(7, win_type='triang').sum()
# df['monthly_average'] = df['compound'].rolling(30, win_type='triang').sum()

# print(df)