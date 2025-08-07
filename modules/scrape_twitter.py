import tweepy
import time
import os
import csv
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# ====== CONFIG ======
BEARER_TOKEN = os.getenv("X_BEARER_TOKEN")

client = tweepy.Client(bearer_token=BEARER_TOKEN)

# Define your prioritized queries
QUERIES = [
    '"LeapScholar" lang:en -is:retweet',
    '"LeapScholar" "IELTS" lang:en -is:retweet',
    '"LeapScholar" "study abroad" lang:en -is:retweet',
    '"LeapScholar" "review" lang:en -is:retweet',
    '"LeapScholar" refund lang:en -is:retweet'
]

# Total max tweets to fetch (across all queries)
MAX_TOTAL_TWEETS = 100
TWEETS_PER_QUERY = MAX_TOTAL_TWEETS // len(QUERIES)

# Store results
all_tweets = []

for query in QUERIES:
    print(f"\nSearching for: {query}")
    try:
        tweets = client.search_recent_tweets(
            query=query,
            tweet_fields=["created_at", "author_id", "public_metrics", "text"],
            max_results=TWEETS_PER_QUERY
        )
    except Exception as e:
        print(f"Error fetching tweets for query: {query} → {e}")
        continue

    if tweets.data:
        for tweet in tweets.data:
            tweet_info = {
                "query": query,
                "author_id": tweet.author_id,
                "created_at": tweet.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "text": tweet.text.replace("\n", " ").strip(),
                "like_count": tweet.public_metrics["like_count"],
                "retweet_count": tweet.public_metrics["retweet_count"],
                "reply_count": tweet.public_metrics["reply_count"],
                "quote_count": tweet.public_metrics["quote_count"]
            }
            all_tweets.append(tweet_info)
    else:
        print("No tweets found.")

    time.sleep(900)  # Avoid hitting rate limit

# ====== SAVE TO CSV ======

filename = f"data/raw/leapscholar_tweets_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

with open(filename, mode="w", encoding="utf-8", newline="") as csv_file:
    fieldnames = [
        "query", "author_id", "created_at", "text",
        "like_count", "retweet_count", "reply_count", "quote_count"
    ]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for tweet in all_tweets:
        writer.writerow(tweet)

print(f"\nSaved {len(all_tweets)} tweets to '{filename}'")

