import praw
import csv
from csv import writer, reader
from datetime import datetime, timedelta

reddit = praw.Reddit(client_id='89t0Tjzp4YkOenLbtGjJpw', 
                     client_secret='MBLF8lTJgLhBHIlq1v2sa9HHVw69eg', 
                     user_agent='Testing_API')
    

filename = 'reddit_hot_posts.csv'
LIMIT = 2000

unique_subreddits = {}
def load_posts(from_file):
    '''
    this method loads all the csv content/lines from the file provided 
    and saves it into a dictionary with key as first column and value the entire row.
    '''
    result = {}
    with open(from_file) as csv_file:
        csv_reader = reader(csv_file, delimiter=',')
        for post in csv_reader:
            result[post[0]] = post
            if post[13] not in unique_subreddits:
                unique_subreddits[post[13]] = list(reddit.info([post[13]]))[0].display_name
                print(f'Found displayname for {post[13]} as {unique_subreddits[post[13]]}')
            post.append(unique_subreddits[post[13]])    

        # if header in the dictionary, remove it
        if "post_id" in result:        
            del result["post_id"]
    return result        

posts = load_posts(filename)
print(f'Loaded {len(posts)} posts and {len(unique_subreddits)} from file {filename}')
error = 0

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
    "subreddit_display_name"
]

with open(filename, 'w') as f:
    w = writer(f)
    w.writerow(header)
    for post in posts.values():
        w.writerow(post)

print(f'Saved {len(posts)} posts into file {filename}')
