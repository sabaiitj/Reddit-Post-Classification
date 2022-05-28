import praw
import csv
from csv import writer
import logging
from datetime import datetime, timedelta

reddit = praw.Reddit(client_id='89t0Tjzp4YkOenLbtGjJpw', 
                     client_secret='MBLF8lTJgLhBHIlq1v2sa9HHVw69eg', 
                     user_agent='Testing_API')
    

filename = 'reddit_hot_posts1.csv'
LIMIT = 1000

def load_posts(from_file):
    posts = {}
    with open(from_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for post in csv_reader:
            posts[post[0]] = post

        if "post_id" in posts:        
            del posts["post_id"]
    return posts        

posts = load_posts(filename)
print(f'Loaded {len(posts)} posts from file {filename}')
error = 0

with open(filename + '.dump', 'w') as f:
    w = writer(f)
    hot_posts = reddit.subreddit('all').hot(limit=LIMIT)
    for post in hot_posts:
        try:
            time_in_mins = round((datetime.utcnow() - datetime.fromtimestamp(post.created)).seconds/60)
            row = [
                post.id,
                post.author.comment_karma,
                post.author.link_karma,# 3
                time_in_mins,
                post.is_original_content, # 6
                post.name, # 9
                post.num_comments,
                post.over_18,
                post.score, # 12
                post.selftext is None, 
                post.spoiler,
                post.stickied,
                post.subreddit.id,
                post.subreddit.name,
                post.subreddit.subscribers,
                post.title,
                post.upvote_ratio,
                post.url,
            ]
            if post.id in posts:
                print(f'Updating {post.id}:{post.title} post.')
            else:
                print(f'Found new post {post.id}:{post.title}.')
            posts[post.id] = row
            w.writerow(row)
        except Exception:
            # Skiping post with incorrect data.
            error += 1
    #         logging.exception("Error reading row", post)
    
        

print(f'Posts with error {error}')

header = [
    "post_id",
    "author_comment_karma",
    "author_link_karma",
    "time_in_mins",
    "post_is_original_content",
    "post_name",
    "post_num_comments",
    "post_over_18",
    "post_score",
    "post_has_link", 
    "post_spoiler",
    "post_stickied",
    "subreddit_id",
    "subreddit_name",
    "subreddit_subscriber_count",
    "post_title",
    "post_upvote_ratio",
    "post_url",
]
posts = load_posts(filename + '.dump')
with open(filename, 'w') as f:
    w = writer(f)
    w.writerow(header)
    for post in posts.values():
        w.writerow(post)

print(f'Saved {len(posts)} posts into file {filename}')        

