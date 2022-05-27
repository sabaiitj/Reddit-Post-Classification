import praw
# import pandas as pd
import csv
from csv import writer

reddit = praw.Reddit(client_id='89t0Tjzp4YkOenLbtGjJpw', 
                     client_secret='MBLF8lTJgLhBHIlq1v2sa9HHVw69eg', 
                     user_agent='Testing_API')

with open('reddit_hot_posts.csv', 'a') as f:
    w = writer(f)
    hot_posts = reddit.subreddit('all').hot(limit=10)
    for post in hot_posts:
        row = [
            post.author.comment_karma,
            post.author.created_utc,
            post.author.is_gold,
            post.author.is_mod,
            post.author.link_karma,
            post.created_utc,
            post.distinguished,
            post.edited,
            post.id,
            post.is_original_content,
            post.is_self,
            post.locked,
            post.name,
            post.num_comments,
            post.over_18,
            post.score,
            post.selftext,
            post.spoiler,
            post.stickied,
            post.subreddit.subscribers,
            post.title,
            post.upvote_ratio,
            post.url,
        ]
        w.writerow(row)
        print(row)
    w.close()

# posts_df = pd.DataFrame(posts,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created', 'distinguished'])
# print(posts_df)

# write to csv

