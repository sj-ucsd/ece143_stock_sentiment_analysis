'''
This script was designed to run inside the parent directory of the 
twitter directory
'''
import pandas as pd 
import os
from statistics import mean
from datetime import datetime
import sys

main_WorkingDir=os.path.abspath(os.curdir)#current working Directory
avg_Dir = os.path.join(main_WorkingDir,"twitter_avgData")

if not os.path.isdir(avg_Dir):
    # directory does not exist so create directory
    os.mkdir(avg_Dir)

# stocks_acronym = ['PANW','AMT','ADI','TMUS','AAPL','ERIC','QCOM','SQ','OKTA','COUP','MELI',
#                         'PYPL','BABA', 'SHOP','NVDA','CRM','AMZN','MSFT','GOOGL','GME','AMC']
#stocks_acronym = ['GME','AMC']

stocks_name = ['Palo Alto Networks','American Tower','Analog Devices','T-Mobile','Apple','Ericsson','Qualcomm',
                'Square','Okta','Coupa Software','MercadoLibre','Paypal','Alibaba','Shopify','NVIDIA',
                'Salesforce','Amazon','Microsoft','Google']

for stock in stocks_acronym:
    os.chdir(main_WorkingDir)
    twit_file = stock + ".csv"
    twit_df = pd.read_csv(twit_file)
    os.chdir(avg_Dir)

    # Get averages for days from both dataframes
    DateToSentiment_dict = {}
    timestamp_key = 'Datetime'
    sentiment_val = 'compound'

    for ind, row in twit_df.iterrows():
        cur_date = str(row[timestamp_key])[0:10]
        if cur_date.count('/')!=2:
            if cur_date.count('-')!=2:
                continue
        if any(char.isalpha() for char in cur_date):
            continue
        if cur_date in DateToSentiment_dict:
            # key already exist
            DateToSentiment_dict[cur_date].append(row[sentiment_val])
        else:
            # key does not exist
            DateToSentiment_dict[cur_date] = [row[sentiment_val]]

    # Dont need to order this data because Twitter data was chronologically collected

    # dictionary now has all data from both dataframes
    # now create dataframe for averages
    avg_df = pd.DataFrame(columns = ['Date','Daily average','weekly average','monthly average'])

    for date in DateToSentiment_dict:
        temp_data = {'Date' : [date],'Daily average' : [mean(DateToSentiment_dict[date])]}
        temp_df = pd.DataFrame(temp_data)
        avg_df = avg_df.append(temp_df,ignore_index=True)

    #avg_df.to_csv('clean_AAPL_twit.csv',index=False)

    # fix dates if issue with it
    date_format = "%Y-%m-%d"
    date_format2 = "%d/%m/%Y"
    for ind,row in avg_df.iterrows():
        try:
            datetime.strptime(row['Date'],date_format)
        except ValueError:
            avg_df.drop(index=ind,inplace=True)
            # print("Before")
            # print(avg_df.at[ind-1,'Date'])
            # print(avg_df.at[ind,'Date'])
            # print(avg_df.at[ind+1,'Date'])
            # temp_date = datetime.strptime(row['Date'],date_format2)
            # avg_df.at[ind,'Date'] = str(temp_date.year) + '-' + str(temp_date.month) + '-' + str(temp_date.day)
            # print("Value")
            # print(str(temp_date.year) + '-' + str(temp_date.month) + '-' + str(temp_date.day))
            # print("after")
            # print(avg_df.at[ind-1,'Date'])
            # print(avg_df.at[ind,'Date'])
            # print(avg_df.at[ind+1,'Date'])

    # compute weekly average and monthly average
    avg_df['Date'] = avg_df['Date'].apply(lambda x: datetime.strptime(x,'%Y-%m-%d'))
    avg_df = avg_df.set_index('Date')
    dates = pd.date_range(avg_df.index[0], avg_df.index[-1], freq='D')

    avg_df = avg_df.reindex(dates) 
    avg_df.reindex(dates)

    avg_df['Daily average'] = avg_df['Daily average'].interpolate(method='pad')
    avg_df['weekly average'] = avg_df['Daily average'].rolling(7, win_type='triang').sum()
    avg_df['monthly average'] = avg_df['Daily average'].rolling(30, win_type='triang').sum()
    avg_df['long term average'] = avg_df['Daily average'].rolling(120, win_type='triang').sum()
    avg_df['mid term average'] = avg_df['Daily average'].rolling(60, win_type='triang').sum()
    avg_df['short term average'] = avg_df['weekly average']

    #print(avg_df.tail(50))
    avg_df.to_csv(stock + '_avg.csv')