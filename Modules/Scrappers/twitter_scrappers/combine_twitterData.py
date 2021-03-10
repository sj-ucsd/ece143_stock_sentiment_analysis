import pandas as pd 
import os
from statistics import mean
from datetime import datetime
from numpy import nan

def combineTwitter_data():
    # Get file paths and directories
    twit_scrapper_dir=os.path.abspath(os.curdir)#current working Directory
    repo_Dir = os.path.dirname(os.path.dirname(os.path.dirname(twit_scrapper_dir)))
    data_Dir = os.path.join(repo_Dir,"Data")
    twit_Dir = os.path.join(data_Dir,"Twitter_data")

    clean_Dir = os.path.join(twit_Dir,"cleanTwitter_Data")

    avg_df = True
    os.chdir(clean_Dir)
    for filename in os.listdir(clean_Dir):
        if not isinstance(avg_df,pd.DataFrame) :
            avg_df = pd.read_csv(filename)
        else:
            temp_df = pd.read_csv(filename)
            avg_df = avg_df.append(temp_df)

    avg_df["Stock Filename"]= nan
    ind = 0
    for filename in os.listdir(clean_Dir):
        avg_df.at[ind,'StockFilename'] = filename
        ind+=1
    os.chdir(twit_Dir)
    avg_df.to_csv('allTwitterStock.csv')

if __name__ == "__main__":
    combineTwitter_data()