'''
This script was designed to run inside the parent directory of the 
submission and comments directories.
'''
import pandas as pd 
import os
from statistics import mean
from datetime import datetime

# Get file paths and directories
main_WorkingDir=os.path.abspath(os.curdir)#current working Directory
sub_Dir = os.path.join(main_WorkingDir,"submission_data")
com_Dir = os.path.join(main_WorkingDir,"comments_data")
avg_Dir = os.path.join(main_WorkingDir,"sentiment_avg")

#os.mkdir(avg_Dir)

com_file = "AAPL_com.csv"
sub_file = "AAPL_sub.csv"

os.chdir(sub_Dir)
sub_df = pd.read_csv(sub_file)

os.chdir(com_Dir)
com_df = pd.read_csv(com_file)

os.chdir(avg_Dir)

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

#avg_df.to_csv('clean_AAPL_sub.csv',index=False)



# compute weekly average and monthly average
for ind, row in avg_df.iterrows():
    cur_date = row['Date']
    print(cur_date)
    day_num = datetime.strptime(cur_date, '%Y-%m-%d').day
    print(day_num)
    input("")