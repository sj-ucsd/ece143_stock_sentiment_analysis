# ece143_stock_sentiment_analysis

## Overview

This project analyzes effect of sentiment from various sources on stock price. See [Project presentation](https://github.com/sj-ucsd/ece143_stock_sentiment_analysis/blob/95b8fc88811a273b48e98c742d9899710c6e220d/ECE143-Group19_Project_presentation.pdf) for details. 

![Pipeline](https://user-images.githubusercontent.com/78191747/110584695-7bc13f00-8124-11eb-9d63-6fef44b5e0d0.png)

## Project organization

* Top level - contains:
  1. Stock_data_visualization - Jupyter-notebook to visualize stock data and models
  2. ECE143-Group19_Project_presentation - Project presentation
  3. ece143_Group19_Assignment6 - Jupyter-notebook for validation and functional tests for week 6
* stock_modules - contains reusable python modules to retrieve sentiment and process stock financials
* Data - contains processed sentiment and financial information for reuse

## Usage

Install the modules described by requirements.txt before running the Visualization notebook

## Modules

### prep_data
Module provides APIs extracts financial information for stocks and prepare the data. APIs are:

1. get_stock_price - Get historical stock price for a given stock over specified period
2. get_earnings_data - load earnings data for specified stock from stored CSV file. 
3. prepare_output_data - create moving average for weekly, monthly and long term and shift by the same amount to match predicted output
4. prepare_output_labels - create three labels (up, down, neutral) on output data 

### ml_models

Module used for MLP model. APIs:

1. apply_MLP - apply MLP model (train and test) and return prediction
2. apply_MLP_on_all_data - Apply MLP model on all stocks in the list 

### scrapers

Provides scripts to scrape news (Yahoo finance), tweets (Twitter) and posts from reddit. This module also applies sentiment analyzer and produces
sentiment score for analysis:

1. get_yahoo_news - get all articles (backwards) from a specified date for a given stock
2. get_sentiment_from_news - extract sentiment scores from news articles
3. getTwitter_data - Retrieve two years worth of tweets for a list of stocks and extract sentiment information
4. getReddit_data - Retrieve two years worth of tweets for a list of stocks and extract sentiment information




