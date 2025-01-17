import pandas as pd 
import sys
import os
from statistics import mean
from datetime import datetime

def cleanReddit_data():
    '''
    Takes the raw Reddit submissions and comments data for each stock and creates a csv file containing
    the daily, weekly, monthly, short term, and long term average sentiment.
    
    Cleaned data is stored in Data/Reddit_data/cleanReddit_data
    '''
    # Get file paths and directories
    red_scrapper_dir=os.path.abspath(os.curdir)#current working Directory
    repo_Dir = os.path.dirname(os.path.dirname(os.path.dirname(red_scrapper_dir)))
    data_Dir = os.path.join(repo_Dir,"Data")
    red_Dir = os.path.join(data_Dir,"Reddit_data")
    raw_dataDir = os.path.join(red_Dir,"reddit_Rawdata")
    clean_data = os.path.join(red_Dir,"cleanReddit_data")

    sub_Dir = os.path.join(raw_dataDir,"submission_Rawdata")
    com_Dir = os.path.join(raw_dataDir,"comments_Rawdata")

    os.chdir(red_Dir)
    if not os.path.isdir(clean_data):
        # directory does not exist so create directory
        os.mkdir(clean_data)

    stocks_acronym = ['PANW','AMT','ADI','TMUS','AAPL','ERIC','QCOM','SQ','OKTA','COUP','MELI',
                            'PYPL','BABA', 'SHOP','NVDA','CRM','AMZN','MSFT','GOOGL']

    stocks_name = ['Palo Alto Networks','American Tower','Analog Devices','T-Mobile','Apple','Ericsson','Qualcomm',
                    'Square','Okta','Coupa Software','MercadoLibre','Paypal','Alibaba','Shopify','NVIDIA',
                    'Salesforce','Amazon','Microsoft','Google']

    for stock in stocks_acronym:
        com_file = stock + "_com.csv"
        sub_file = stock + "_sub.csv"

        os.chdir(sub_Dir)
        sub_df = pd.read_csv(sub_file)

        os.chdir(com_Dir)
        com_df = pd.read_csv(com_file)

        os.chdir(clean_data)


        # https://hackersandslackers.com/pandas-dataframe-drop/
        # # Drop columns for weekly and monthly avg because these were generated incorrectly
        # reddit_df.drop(['weekly_average','monthly_average'], axis=1, inplace=True)

        # # Drop any row that is missing more than one cell with data
        # reddit_df.dropna(how='any',thresh=1,inplace = True)

        # Is it possible for info in dataframe to be fine but be bad in csv file
        #print(sub_df.head(68))


        # Get averages for days from both dataframes
        DateToSentiment_dict = {}
        timestamp_key = 'created'
        sentiment_val = 'compound'

        # get date and compound value for each post
            # if it does exist add sent to dictionary
            # else create a new key and add a list with the current sentiment
        for ind, row in sub_df.iterrows():
            cur_date = row[timestamp_key][0:10]
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

        for ind, row in com_df.iterrows():
            cur_date = row[timestamp_key][0:10]
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

        # # sort dictionary based on date
        orderedTup = sorted(DateToSentiment_dict.items(),key=lambda x:datetime.strptime(x[0],'%Y-%m-%d'))
        # list of tuples
        # orderedTup => [('2019-02-13', [0.0, -0.296, 0.0, 0.0, 0.0, 0.0, -0.296, -0.296])]

        # dictionary now has all data from both dataframes
        # now create dataframe for averages
        avg_df = pd.DataFrame(columns = ['Date','Daily average','weekly average','monthly average'])

        for tup in orderedTup:
            temp_data = {'Date' : [tup[0]],'Daily average' : [mean(tup[1])]}
            temp_df = pd.DataFrame(temp_data)
            avg_df = avg_df.append(temp_df,ignore_index=True)
            

        # compute weekly average and monthly average
        avg_df['Date'] = avg_df['Date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))
        avg_df = avg_df.set_index('Date')
        #dates = pd.date_range(avg_df.index[0], avg_df.index[-1], freq='D')
        dates = pd.date_range('2019-02-13', '2021-02-13', freq='D')

        avg_df = avg_df.reindex(dates) 
        avg_df.reindex(dates)

        avg_df['Daily average'] = avg_df['Daily average'].interpolate(method='pad')
        avg_df['weekly average'] = avg_df['Daily average'].rolling(7, win_type='triang').sum()
        avg_df['monthly average'] = avg_df['Daily average'].rolling(40, win_type='triang').sum()
        avg_df['long term average'] = avg_df['Daily average'].rolling(90, win_type='triang').sum()
        #avg_df['mid term average'] = avg_df['Daily average'].rolling(60, win_type='triang').sum()
        avg_df['short term average'] = avg_df['weekly average']

        avg_df.to_csv(stock + '_avg.csv')

if __name__ == "__main__":
    cleanReddit_data()