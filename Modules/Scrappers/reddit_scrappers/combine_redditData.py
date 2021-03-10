import pandas as pd 
from numpy import nan
import os
from statistics import mean
from datetime import datetime

def combineReddit_data():
    '''
    Takes each stocks average sentiment csv files and stacks them vertically. Then saves it to a
    csv file containing all stocks.

    Csv file is stored in Data/Reddit_data
    '''
    # Get file paths and directories
    red_scrapper_dir=os.path.abspath(os.curdir)#current working Directory
    repo_Dir = os.path.dirname(os.path.dirname(os.path.dirname(red_scrapper_dir)))
    data_Dir = os.path.join(repo_Dir,"Data")
    red_Dir = os.path.join(data_Dir,"Reddit_data")
    clean_data = os.path.join(red_Dir,"cleanReddit_data")

    avg_df = True
    os.chdir(clean_data)
    for filename in os.listdir(clean_data):
        if not isinstance(avg_df,pd.DataFrame) :
            avg_df = pd.read_csv(filename)
        else:
            temp_df = pd.read_csv(filename)
            avg_df = avg_df.append(temp_df)

    avg_df["Stock Filename"]= nan
    ind = 0
    for filename in os.listdir(clean_data):
        avg_df.at[ind,'StockFilename'] = filename
        ind+=1
    os.chdir(red_Dir)
    avg_df.to_csv('allRedditStocks.csv')

if __name__ == "__main__":
    combineReddit_data()