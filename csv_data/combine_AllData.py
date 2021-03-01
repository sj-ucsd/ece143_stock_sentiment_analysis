import pandas as pd 
import os
from statistics import mean
from datetime import datetime
from numpy import nan

# Get file paths and directories
main_WorkingDir=os.path.abspath(os.curdir)#current working Directory
red_Dir = os.path.join(main_WorkingDir,"redditStock_data")
redSent_Dir = os.path.join(red_Dir,"sentiment_avg")
twit_Dir = os.path.join(main_WorkingDir,"twitter_data")
twit_avg_Dir = os.path.join(twit_Dir,"twitter_avgData")

avg_df = True
os.chdir(redSent_Dir)
for filename in os.listdir(redSent_Dir):
    if not isinstance(avg_df,pd.DataFrame) :
        avg_df = pd.read_csv(filename)
    else:
        temp_df = pd.read_csv(filename)
        avg_df = avg_df.append(temp_df)

avg_df["Stock Filename"]= nan
ind = 0
for filename in os.listdir(redSent_Dir):
    avg_df.at[ind,'StockFilename'] = filename
    ind+=1


os.chdir(twit_avg_Dir)
for filename in os.listdir(twit_avg_Dir):
    temp_df = pd.read_csv(filename)
    avg_df = avg_df.append(temp_df)


for filename in os.listdir(twit_avg_Dir):
    avg_df.at[ind,'StockFilename'] = filename
    ind+=1
os.chdir(main_WorkingDir)
avg_df.to_csv('RedditANDTwitter_data.csv')