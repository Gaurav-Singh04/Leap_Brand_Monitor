import praw
import os
from dotenv import load_dotenv
load_dotenv()

reddit = praw.Reddit(
    client_id = os.getenv("REDDIT_CLIENT_ID"),
    client_secret = os.getenv("REDDIT_SECRET"),
    password = os.getenv("REDDIT_PASSWORD"),
    user_agent = os.getenv("REDDIT_USER_AGENT"),
    username  = os.getenv("REDDIT_USERNAME"),
)

reddit.read_only = True


import json

def get_comment_tree(comment, max_depth=3, cur_depth=1):
    if cur_depth > max_depth:
        return None
    comment_data = {
        'comment_id': comment.id,
        'comment_text': comment.body,
        'comment_author': str(comment.author),
        'created_utc': comment.created_utc,
        'score': comment.score,
        'replies': []
    }
    if hasattr(comment, 'replies'):
        for reply in comment.replies:
            child = get_comment_tree(reply, max_depth, cur_depth+1)
            if child:
                comment_data['replies'].append(child)
    return comment_data

def fetch_reddit_leapscholar_posts_comments_json(output_json, max_posts=50, max_comments=20, max_depth=3):
    query = "leapscholar"
    posts = reddit.subreddit("all").search(query, sort="new", limit=max_posts)
    data = []
    for post in posts:
        post_dict = {
            'post_id': post.id,
            'post_title': post.title,
            'post_text': post.selftext,
            'post_url': post.url,
            'post_score': post.score,
            'post_num_comments': post.num_comments,
            'created_utc': post.created_utc,
            'author': str(post.author),
            'comments': []
        }
        post.comments.replace_more(limit=0)
        for i, comment in enumerate(post.comments):
            if i >= max_comments:
                break
            comment_tree = get_comment_tree(comment, max_depth=max_depth)
            if comment_tree:
                post_dict['comments'].append(comment_tree)
        data.append(post_dict)
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    fetch_reddit_leapscholar_posts_comments_json("brand_monitor/data/raw/reddit_leapscholar.json")