import numpy as np
import pandas as pd
import os
!pip install yahooquery
import yahooquery
from pandas_datareader import data
from datetime import timedelta, date, datetime

#def get_yahoo_dataframe(symbol,start_date='2020-06-01',end_date='2021-01-29'):
def get_stock_price(symbol,start_date='2020-06-01',end_date='2021-01-29'):
    '''
    :symbol: stock symbol (example: AAPL). Type str
    :start_date: Date from which to get data. Date in string format
    :end_date: Date up to which to get data. Date in string format
    Returns pandas dataframe from consisting of stock price history
    '''
    ticker = yahooquery.Ticker(symbol)
    df=data.DataReader(symbol, 'yahoo', start_date, end_date).reset_index()
    df.set_index(pd.to_datetime(df['Date']), inplace=True)
    df = df.drop(['Date'], axis=1)
    return df

def prepare_data_Y_for_MLP(df, how_long=7):
  # how_long = "weekly": 7, "monthly":40, "Quarterly":90
  advance = df['Adj Close'].shift(-how_long)
  Y = ((advance - df['Adj Close'])/df['Adj Close'])*100
  #Y=Y[how_long:]
  return Y 

def save_yahoo_stock_financial(symlist=['AAPL', 'ADI', 'AMT', 'AMZN', 'BABA', 'COUP', 'CRM', 'ERIC', 'GOOGL', 'MELI', 'MSFT', 'NVDA', 'OKTA', 'PANW', 'PYPL', 'QCOM', 'SHOP', 'SQ', 'TMUS'], how_long_list=[7,40,90]):
  for symbol in symlist:
    # df_x=pd.read_csv('/content/gdrive/My Drive/Colab Notebooks/reddit_avg_data/{}_avg.csv'.format(symbol), index_col=0)
    df=get_yahoo_dataframe(symbol)
    df["short-term stock"]=prepare_data_Y_for_MLP(df, how_long=how_long_list[0])
    df["mid-term stock"]=prepare_data_Y_for_MLP(df, how_long=how_long_list[1])
    df["long-term stock"]=prepare_data_Y_for_MLP(df,how_long=how_long_list[2])
    df.to_csv('../Data/Yahoo_stock_financial/{}_avg.csv'.format(symbol))
