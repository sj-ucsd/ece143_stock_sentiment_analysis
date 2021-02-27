'''
This script was designed to run inside the parent directory of the 
twitter directory
'''
import pandas as pd 
import os
from statistics import mean
from datetime import datetime

main_WorkingDir=os.path.abspath(os.curdir)#current working Directory
avg_Dir = os.path.join(main_WorkingDir,"twitter_avgData")

#os.mkdir(avg_Dir)
os.chdir(main_WorkingDir)
twit_file = "AAPL.csv"
twit_df = pd.read_csv(twit_file)
os.chdir(avg_Dir)

# Get averages for days from both dataframes
DateToSentiment_dict = {}
timestamp_key = 'Datetime'
sentiment_val = 'compound'

for ind, row in twit_df.iterrows():
    cur_date = row[timestamp_key][0:10]
    if cur_date.count('/')!=2:
        if cur_date.count('-')!=2:
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

avg_df.to_csv('clean_AAPL_twit.csv',index=False)


# compute weekly average and monthly average
for ind, row in avg_df.iterrows():
    cur_date = row['Date']
    print(cur_date)
    day_num = datetime.strptime(cur_date, '%Y-%m-%d').day
    print(day_num)
    input("")