import numpy as np
import pandas as pd
import os
# from pandas_datareader import data
from datetime import timedelta, date, datetime

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import seaborn as sn
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import r2_score

import matplotlib.pyplot as plt

import seaborn as sns

symlist = ['AAPL', 'AMT', 'AMZN', 'BABA', 'COUP', 'CRM', 'ERIC', 'GOOGL', 'MELI', 'MSFT', 'NVDA', 'OKTA', 'PANW', 'PYPL', 'QCOM', 'SHOP', 'SQ', 'TMUS']
# symbol=symlist[0]
# Append all stocks along the rows and redefine the index
# weekly_or_monthly = 'monthly'
data_type = 'twitter' # reddit, twitter, yahoo
how_long_list = [7,40,90]
how_long_text = ['weekly', 'monthly', 'quarterly']
term_stock = ['weekly stock', 'monthly stock', 'quarterly stock']
term_sentiment = ['Weekly Sentiment', 'Monthly Sentiment', 'Quarterly Sentiment']
column_list = ['Short Term', 'Mid Term', 'Long Term']

twit_sentiment_list = ['weekly average', 'monthly average', 'long term average']
twit_stock_list = ['short-term stock', 'mid-term stock', 'long-term stock']

# how_long = "weekly": 7, "monthly":40, "Quarterly":90
df_r2_all=[]
for idx,how_long in enumerate(how_long_list):
  # weekly_or_monthly=how_long_text[idx]
  append_df=[] #list of dataframes
  append_X=[]
  append_Y=[]
  for symbol in symlist:
    dfy=pd.read_csv('/content/gdrive/My Drive/Colab Notebooks/yahoo_stock_ground_truth/{}_avg.csv'.format(symbol), index_col=0)
    dfy.interpolate(limit_direction='both',inplace=True)
    if data_type=='yahoo':
      df=pd.read_csv('/content/gdrive/My Drive/Colab Notebooks/yahoo_all_data/{}.csv'.format(symbol), index_col=0)
      X = df[['Adj Close','Volume', 'Surprise_EPS',term_sentiment[idx]]]#'Total Sentiment','Avg Sentiment'
      Y = df[term_stock[idx]]
    elif data_type=='twitter': #need to fix bug in twitter data
      dft=pd.read_csv('/content/gdrive/My Drive/Colab Notebooks/twitter_avgData/{}_Twitavg.csv'.format(symbol), index_col=0)
      dft.drop(dft.index[-1],inplace=True)
      dft.interpolate(limit_direction='both',inplace=True)
      X = pd.concat([dft[[twit_sentiment_list[idx]]], dfy[['Adj Close','Volume']]],axis=1)
      X.interpolate(limit_direction='both',inplace=True)
      Y = dfy[twit_stock_list[idx]]
    elif data_type=='reddit':
      dfr=pd.read_csv('/content/gdrive/My Drive/Colab Notebooks/sentiment_avg/{}_avg.csv'.format(symbol), index_col=0)
      dfr.drop(dfr.index[-1],inplace=True)
      dfr.interpolate(limit_direction='both',inplace=True)
      X = pd.concat([dfr[[twit_sentiment_list[idx]]], dfy[['Adj Close','Volume']]],axis=1)
      Y = dfy[twit_stock_list[idx]]
    # Y=prepare_data_Y_for_ML(df, how_long)
    append_Y.append(Y)
    # X=prepare_data_X_for_ML(df, how_long)
    #X.drop(['Adj Close', 'Volume'], axis=1, inplace=True)
    append_X.append(X)
    #print(df.shape)
    #df=df.drop(['Date','Estimated_Revenue','Reported_Revenue','Estimated_EPS','Reported_EPS','Period Ending'],axis=1)
    # append_df.append(df)
  
  # df2=pd.concat(append_df)
  # df2.shape

  Xall=pd.concat(append_X)
  Xall.interpolate(limit_direction='both',inplace=True)
  Yall=pd.concat(append_Y)
  Yall.rename('Ground Truth', inplace=True)
  # Train on all  data
  X_train,X_test,y_train,y_test = train_test_split(Xall,Yall,test_size=0.25,random_state=0)
  out=apply_MLP(X_train,X_test,y_train,y_test)
  r2score_all=r2_score(out['Ground Truth'], out['Prediction'])
  #print(out)
  print("The Score All ", (r2_score(out['Ground Truth'], out['Prediction'])))

  #Train individually 
  r2score_list = []
  for si,symbol in enumerate(symlist):
    df=pd.read_csv('/content/gdrive/My Drive/Colab Notebooks/yahoo_prepared_df/{}.csv'.format(symbol), index_col=0)
    X=append_X[si]
    Y=append_Y[si]
    Y.rename('Ground Truth', inplace=True)
    # Y=prepare_data_Y_for_ML(df,  how_long)
    # X=prepare_data_X_for_ML(df,  how_long)
    #X.drop(['Adj Close', 'Volume'], axis=1, inplace=True)
    #X=X.drop(['Adj Close'],axis=1)
    X_train,X_test,y_train,y_test = train_test_split(X,Y,test_size=0.25,random_state=0)
    out=apply_MLP(X_train,X_test,y_train,y_test)
    print("The Score Individual ", (r2_score(out['Ground Truth'], out['Prediction'])))
    r2score_list.append(r2_score(out['Ground Truth'], out['Prediction']))
  df_r2 = pd.DataFrame({'r2':r2score_list}, index=symlist)
  df_r2=df_r2.append(pd.DataFrame({'r2':r2score_all}, index=['All Stocks']))
  df_r2.rename(columns={'r2':column_list[idx]}, inplace=True)
  df_r2_all.append(df_r2)

  company_list={
  "AAPL":"Apple",
  "ADI": "Analog Devices",
  "AMT": "American Tower",
  "AMZN": "Amazon",
  "BABA": "Alibaba",
  "COUP": "Coupa Software",
  "CRM": "Salesforce",
  "ERIC": "LM Ericsson",
  "GOOGL": "Alphabet",
  "MELI": "MercadoLibre",
  "MSFT": "Microsoft",
  "NVDA": "Nvidia",
  "OKTA": "Okta",
  "PANW": "Palo Alto Networks",
  "PYPL": "PayPal",
  "QCOM": "Qualcomm",
  "SHOP": "Shopify",
  "SQ": "Square",
  "TMUS": "T-Mobile"}

  aa=sns.color_palette()

  clr_list = pd.DataFrame( [[aa[0]]]*19,index = symlist, columns=['color'])
  # clr_list.append
  clr_list=clr_list.append(pd.DataFrame({'color':[aa[3]]}, index=['All Stocks']))
  df_r2_all.append(clr_list)
  mydf = pd.concat(df_r2_all,axis=1)
  mydf.rename(company_list, inplace=True)
  mydf.sort_values(by=column_list[1],axis=0,inplace=True,ascending=True)
  mydf.to_csv('/content/gdrive/My Drive/Colab Notebooks/figures/'+data_type+'.csv')