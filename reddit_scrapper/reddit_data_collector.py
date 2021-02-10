#https://www.storybench.org/how-to-scrape-reddit-with-python/
#https://praw.readthedocs.io/en/latest/code_overview/models/subreddit.html#praw.models.Subreddit.submissions

# Email log in:
# John Doe
# email: john394doe924@gmail.com
# Pass: ECE143$$project
# DOB: June 1, 1990
# Male

# Reddit log in:
# username: johnd394
# Pass: ECE143$$project

import praw
import pandas as pd 
import datetime as dt 

reddit = praw.Reddit(client_id='URIdyR70yWXXGA', \
                    client_secret='LzgXHl91m7hvDB3euI-bYV_SmC72EQ', \
                    user_agent='ECE143_redditData', \
                    username='johnd394', \
                    password='ECE143$$project')


# Search based off of specific subreddit
list_subreddits = ['all','investing', 'stocks','wallstreetbets']

# Keys
key = 'QCOM'

# Dictionary for information
topics_dict = { "title":[], "score":[], "id":[], "url":[], "comms_num": [], "created": [], "body":[]}

# sort
list_sorts = ['relevance','hot','top','new','comments']
#relevance, hot, top, new, comments. (default: relevance).

#https://praw.readthedocs.io/en/latest/code_overview/models/subreddit.html?highlight=search#praw.models.Subreddit.search
# Search all subreddits
cnt=0
for sub_ele in list_subreddits:
    subred = reddit.subreddit(sub_ele)
    for sort_ele in list_sorts:
        search_res = subred.search(key,sort=sort_ele,time_filter='year',limit=None)
        for res_ele in search_res:
            cnt+=1
            # print(dir(res_ele))
            #break
            topics_dict["title"].append(res_ele.title)
            topics_dict["score"].append(res_ele.score)
            topics_dict["id"].append(res_ele.id)
            topics_dict["url"].append(res_ele.url)
            topics_dict["comms_num"].append(res_ele.num_comments)
            topics_dict["created"].append(res_ele.created)
            topics_dict["body"].append(res_ele.selftext)
        #break
    #break
#print(topics_dict)
print(cnt)
# topics_data = pd.DataFrame(topics_dict)

# topics_data.to_csv('redditData.csv', index=False) 