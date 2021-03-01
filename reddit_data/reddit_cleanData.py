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

if not os.path.isdir(avg_Dir):
    # directory does not exist so create directory
    os.mkdir(avg_Dir)

# stocks_acronym = ['PANW','AMT','ADI','TMUS','AAPL','ERIC','QCOM','SQ','OKTA','COUP','MELI',
#                         'PYPL','BABA', 'SHOP','NVDA','CRM','AMZN','MSFT','GOOGL']
stocks_acronym = ['GME','AMC']

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
    dates = pd.date_range(avg_df.index[0], avg_df.index[-1], freq='D')

    avg_df = avg_df.reindex(dates) 
    avg_df.reindex(dates)

    avg_df['Daily average'] = avg_df['Daily average'].interpolate(method='pad')
    avg_df['weekly average'] = avg_df['Daily average'].rolling(7, win_type='triang').sum()
    avg_df['monthly average'] = avg_df['Daily average'].rolling(30, win_type='triang').sum()
    avg_df['long term average'] = avg_df['Daily average'].rolling(120, win_type='triang').sum()
    avg_df['mid term average'] = avg_df['Daily average'].rolling(60, win_type='triang').sum()
    avg_df['short term average'] = avg_df['weekly average']

    #avg_df.to_csv('clean_AAPL_sub.csv',index=False)
    avg_df.to_csv(stock + '_avg.csv')






# Mudit's code
# # avg_df[[avg_df.columns[-3],avg_df.columns[-2],avg_df.columns[-1] ]]
# # X = avg_df[[avg_df.columns[-3],avg_df.columns[-2],avg_df.columns[-1] ]]
# # Y=prepare_data_Y_for_ML(df)
# # X=prepare_data_X_for_ML(df)
# # X_train,X_test,y_train,y_test = train_test_split(X,Y,test_size=0.25,random_state=0)
# # out=apply_MLP(X_train,X_test,y_train,y_test)
# symbol = 'AAPL'
# df = get_yahoo_dataframe(symbol)
# os.chdir('/home/muditj/Desktop/ECE143/ece143_stock_sentiment_analysis/')
# stock_file = process_stock_data('./earnings_data/AAPL.csv', df)
# df = df.join(stock_file)
# df = df.reindex(pd.date_range(avg_df.index[0], avg_df.index[-1], freq='D'))
# for i in df.columns:
#     df[i] = df[i].interpolate(method='pad')
# plt.figure(figsize=(12,5))
# plt.xlabel('Dates')
# ax1 = out[\"Prediction\"].plot(color='blue', grid=True)
# ax2 = out[\"Ground Truth\"].plot(color='red', grid=True)
# h1, l1 = ax1.get_legend_handles_labels()
# h2, l2 = ax2.get_legend_handles_labels()
# plt.legend(h1, l1, loc=2)
# plt.show()
# df = df.drop('Estimated_Revenue', axis=1)
# df = df.drop('Reported_Revenue', axis=1)
# df = df.drop('Date', axis=1)
# df = df.drop('Estimated_EPS', axis=1)
# df = df.drop('Reported_EPS', axis=1)
# df = df.drop('Period Ending', axis=1)
# # Test SVM (ToDo: One hot coding and SVM)
# # avg_df= avg_df.drop('weekly average', axis=1)
# # avg_df = avg_df.drop('monthly average', axis=1)
# # avg_df = avg_df.drop('long term average', axis=1)
# #df = df.drop('short term average', axis=1)
# #df= df.drop('mid term average', axis=1)
# #df=df.drop('Daily average', axis=1)
# df = df.join(avg_df)
# def prepare_data_Y_for_ML2(df):
#     output = df['Adj Close']
#     output.rename('Stock Price')
#     advance = df['Adj Close'].shift(7)
#     advance = advance.rename('Short Term Advance')
#     advance2 = df['Adj Close'].shift(40)
#     advance2 = advance2.rename('Mid Term Advance')
#     gt = pd.concat([output, advance, advance2], axis=1)
#     gt['Short Term Change'] = ((gt['Short Term Advance'] - gt['Adj Close'])/gt['Adj Close'])*100
#     gt['Mid Term Change'] = ((gt['Mid Term Advance'] - gt['Adj Close'])/gt['Adj Close'])*100
#     #print(gt[9:110])
#     gt['Short Term Change'].plot()
#     Y = gt['Mid Term Change'][400:]
#     return Y

# Y = prepare_data_Y_for_ML2(df)
# max(Y)
# min(Y)
# X = df[400:]
# #X = X.drop('mid term average',axis=1)
# #X = X.drop('short term average', axis=1)
# X_train,X_test,y_train,y_test = train_test_split(X,Y,test_size=0.15,random_state=0)
# sc_X = StandardScaler()
# X_trainscaled=sc_X.fit_transform(X_train)
# X_testscaled=sc_X.transform(X_test)
# reg = MLPRegressor(hidden_layer_sizes=(5,6,5),activation=\"relu\" ,random_state=1, max_iter=3000).fit(X_trainscaled, y_train)
# y_pred=reg.predict(X_testscaled)
# print(\"The Score with \", (r2_score(y_pred, y_test)))
# y_pred = pd.DataFrame(y_pred)
# out = pd.concat([y_test.reset_index(drop=True),y_pred.reset_index(drop=True)], axis=1)
# out = out.rename(columns={0:\"Prediction\", \"Mid Term Change\":\"Ground Truth\"})
# # out=apply_MLP(X_train,X_test,y_train,y_test)
# plt.figure(figsize=(12,5))
# plt.xlabel('Dates')
# ax1 = out[\"Prediction\"].plot(color='blue', grid=True)
# ax2 = out[\"Ground Truth\"].plot(color='red', grid=True)
# #ax3 = Y.reset_index(drop=True).plot(color='green', grid=True)
# h1, l1 = ax1.get_legend_handles_labels()
# h2, l2 = ax2.get_legend_handles_labels()
# h2, l2 = ax3.get_legend_handles_labels()
# plt.legend(h1, l1, loc=2)
# plt.show()
