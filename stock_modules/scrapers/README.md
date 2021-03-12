# Scrapers

## reddit_scrapers

This directory contains scripts for collecting and analyzing data from Reddit.

- combine_redditData.py - Takes all the cleaned data with the average sentiment and stacks each stocks data vertically in a csv file.
- reddit_cleanData.py - Takes the raw reddit data for each stock and creates a csv for each stock showing the average sentiment for different time periods.
- reddit_scrapper.py - Collects 2 years of reddit data using the PSAW API for each stock and creates a csv file containing it.

## twitter_scrapers

This directory contains scripts for collecting and analyzing data from Twitter.

- combine_twitterData.py - Takes all the cleaned data with the average sentiment and stacks each stocks data vertically in a csv file.
- twitter_cleanData.py - Takes the raw twitter data for each stock and creates a csv for each stock showing the average sentiment for different time periods.
- twitter_scrapper - Collects 2 years of twitter data for each stock and creates a csv file containing it.

## news_scraper.py
news_scraper provides functions to extract news articles from Yahoo Finance and compute sentiment on them. 
