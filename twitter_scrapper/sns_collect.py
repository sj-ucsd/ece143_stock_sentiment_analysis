import pandas as pd
import snscrape.modules.twitter as sntwitter
import itertools

# https://medium.com/swlh/how-to-scrape-tweets-by-location-in-python-using-snscrape-8c870fa6ec25
# do more using sns
# https://medium.com/better-programming/how-to-scrape-tweets-with-snscrape-90124ed006af

# our search term, using syntax for Twitter's Advanced Search
search = '"American Tower"'

# the scraped tweets, this is a generator
scraped_tweets = sntwitter.TwitterSearchScraper(search+' since:2020-09-01 until:2020-09-05').get_items()

# slicing the generator to keep only the first 100 tweets
sliced_scraped_tweets = itertools.islice(scraped_tweets, 50)

# convert to a DataFrame and keep only relevant columns
df = pd.DataFrame(sliced_scraped_tweets)[['date', 'content']]

#lines above can be shortened to 
# pd.DataFrame(itertools.islice(sntwitter.TwitterSearchScraper('"data science"').get_items(), 100))

df.to_csv('sns_twitter.csv',index=False)