#https://melaniewalsh.github.io/Intro-Cultural-Analytics/Data-Collection/Reddit-Data-Collection-With-PSAW.html
#https://github.com/dmarx/psaw
import pandas as pd 
from psaw import PushshiftAPI
import praw
import datetime as dt

r = praw.Reddit(client_id='URIdyR70yWXXGA', \
                    client_secret='LzgXHl91m7hvDB3euI-bYV_SmC72EQ', \
                    user_agent='ECE143_redditData', \
                    username='johnd394', \
                    password='ECE143$$project')

api = PushshiftAPI(r)

start_epoch=int(dt.datetime(2020, 1, 1).timestamp())
end_epoch=int(dt.datetime(2020, 1, 10).timestamp())

# temp = api.search_submissions(after=start_epoch,
#                             subreddit='politics',
#                             filter=['url','author', 'title', 'subreddit'],
#                             limit=10)

api_request_generator = api.search_submissions(q='QCOM',after=start_epoch,before=end_epoch,filter=['url','author', 'title', 'subreddit'],limit=10)

collected_submissions = pd.DataFrame([submission.d_ for submission in api_request_generator])
collected_submissions['date'] = pd.to_datetime(collected_submissions['created_utc'], utc=True, unit='s')
print(collected_submissions[['author', 'date', 'title', 'selftext', 'url', 'subreddit', 'score', 'num_comments', 'num_crossposts', ]])
print(collected_submissions['subreddit'].value_counts())

