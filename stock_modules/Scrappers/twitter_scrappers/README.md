# twitter_scrappers

## twitter_scrapper.py

This script collects two years of data for each stock. Each day all tweets involving the stocks name in its body is collected. Applying sentiment analysis on the text body for each tweet that is collected. 

## twitter_cleanData.py

This script loads the collected data for each stock from twitter_scrapper.py and applies further cleaning/analysis to get a better representation of our collected raw data.

## combine_twitterData.py

This script loads the cleaned data output from twitter_cleanData.py and stacks all the stocks vertically for our model.