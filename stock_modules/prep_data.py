import numpy as np
import pandas as pd
import os
import yahooquery
from pandas_datareader import data
from datetime import timedelta, date, datetime

def get_stock_price(symbol,start_date='2020-06-01',end_date='2021-01-29'):
    '''
    :symbol: stock symbol (example: AAPL). Type str
    :start_date: Date from which to get data. Date in string format
    :end_date: Date up to which to get data. Date in string format
    Returns pandas dataframe from consisting of stock price history
    '''
    assert isinstance(symbol, str)
    assert isinstance(start_date, str)
    assert isinstance(end_date, str)
    ticker = yahooquery.Ticker(symbol)
    df=data.DataReader(symbol, 'yahoo', start_date, end_date).reset_index()
    df.set_index(pd.to_datetime(df['Date']), inplace=True)
    df = df.drop(['Date'], axis=1)
    return df

def prepare_output_data(df, length=7):
  '''
  :df: Pandas dataframe with stock price information
  :length: length over which price change to be calculated
  returns a pandas series with price change information
  length = "weekly": 7, "monthly":40, "Quarterly":90
  '''
  assert isinstance(length, int)
  assert isinstance(df,pd.DataFrame)
  assert 'Adj Close' in df.columns
  assert length > 0
  assert length < df.shape[0]

  advance = df['Adj Close'].shift(-length)
  Y = ((advance - df['Adj Close'])/df['Adj Close'])*100
  return Y 

def prepare_output_labels(df,length=7, threshold=1):
  '''
  :df: Pandas dataframe with stock price
  :length: over which price change to be calculated
  :threshold: percentage used to create labels. For example:
  threshold 1 means if > 1% use label 'up', < 1% use label 'down' 
  and if in between use label 'neutral
  '''
  assert isinstance(length, int)
  assert isinstance(df,pd.DataFrame)
  assert 'Adj Close' in df.columns
  assert isinstance(threshold, int)
  tmp_df = df['Adj Close'].to_frame()
  tmp_df['price_change'] = prepare_output_data(df, length)
  tmp_df['price_labels'] = tmp_df['price_change']
  #apply thresholds first
  tmp_df.loc[tmp_df['price_change'] >= threshold, 'price_labels' ] = 'up'
  tmp_df.loc[tmp_df['price_change'] <= -threshold, 'price_labels' ] = 'down'
  tmp_df.loc[(tmp_df['price_change']>-threshold)& \
             (tmp_df['price_change']<threshold),'price_labels'] ='neutral'
  return tmp_df['price_labels']

def get_earnings_data(filename, df):
  '''
  :filename: CSV file containing earnings data
  :df: Pandas dataframe with stock price
  returns dataframe containing earnings data - index synchronized with df
  '''
  assert isinstance(df,pd.DataFrame)
  assert isinstance(filename, str)
  
  earnings_data = pd.read_csv(filename)
  earnings_data.set_index(pd.to_datetime(earnings_data['Date']), inplace=True)
  earnings_data = earnings_data.reindex(df.index, method='bfill')
  earnings_data = earnings_data.drop(['Date','Period Ending'], axis=1)
  return earnings_data
  
