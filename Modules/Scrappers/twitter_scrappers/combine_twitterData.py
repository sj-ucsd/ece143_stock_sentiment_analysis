import pandas as pd 
import os
from statistics import mean
from datetime import datetime
from numpy import nan

# Get file paths and directories
main_WorkingDir=os.path.abspath(os.curdir)#current working Directory
twit_Dir = os.path.join(main_WorkingDir,"twitter_data")
twit_avg_Dir = os.path.join(twit_Dir,"cleanTwitter_Data")

avg_df = True
os.chdir(twit_avg_Dir)
for filename in os.listdir(twit_avg_Dir):
    if not isinstance(avg_df,pd.DataFrame) :
        avg_df = pd.read_csv(filename)
    else:
        temp_df = pd.read_csv(filename)
        avg_df = avg_df.append(temp_df)

avg_df["Stock Filename"]= nan
ind = 0
for filename in os.listdir(twit_avg_Dir):
    avg_df.at[ind,'StockFilename'] = filename
    ind+=1
os.chdir(main_WorkingDir)
avg_df.to_csv('allTwitterStock.csv')