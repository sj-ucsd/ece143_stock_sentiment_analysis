# reddit_scrappers

## reddit_scrapper.py

This script collects two years of data for each stock using the PSAW API. Each day within the two year period the top 5 rated posts and comments with the highest score is collected. Applying sentiment analysis on the title and/or body for each post and comment that is collected. 

## reddit_cleanData.py

This script loads the collected data for each stock from reddit_scrapper.py and applies further cleaning/analysis to get a better representation of our collected raw data.

## combine_redditData.py

This script loads the cleaned data output from reddit_cleanData.py and stacks all the stocks vertically for our model.