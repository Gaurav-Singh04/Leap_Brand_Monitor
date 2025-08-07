import csv
import feedparser

LEAP_QUERIES = [
    'LeapScholar',
    'LeapScholar+IELTS',
    'LeapScholar+study+abroad',
    'LeapScholar+review',
    'LeapScholar+refund',
]

KEYWORD_QUERIES = [
    'study+abroad',
    'IELTS',
    'education',
    'scholarship',
]


leap_articles = []
keyword_articles = []

# Scrape for LEAP_QUERIES (for sentiment analysis)
for query in LEAP_QUERIES:
    print(f"Searching Google News RSS for LEAP query: {query}")
    rss_url = f"https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"
    feed = feedparser.parse(rss_url)
    print(f"  Found {len(feed.entries)} articles for '{query}'")
    for entry in feed.entries:
        article_info = {
            "source_name": entry.get("source", {}).get("title") if entry.get("source") else "Google News",
            "title": entry.get("title"),
            "url": entry.get("link"),
        }
        leap_articles.append(article_info)

# Scrape for KEYWORD_QUERIES (for keyword extraction)
for query in KEYWORD_QUERIES:
    print(f"Searching Google News RSS for KEYWORD query: {query}")
    rss_url = f"https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"
    feed = feedparser.parse(rss_url)
    print(f"  Found {len(feed.entries)} articles for '{query}'")
    for entry in feed.entries:
        article_info = {
            "source_name": entry.get("source", {}).get("title") if entry.get("source") else "Google News",
            "title": entry.get("title"),
            "url": entry.get("link"),
        }
        keyword_articles.append(article_info)

# Save LEAP articles for sentiment analysis
leap_filename = "data/raw/leapscholar_news_leap.csv"
with open(leap_filename, mode="w", encoding="utf-8", newline="") as csv_file:
    fieldnames = ["source_name", "title", "url"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for article in leap_articles:
        writer.writerow(article)
print(f"Saved {len(leap_articles)} LEAP news articles to '{leap_filename}'")

# Save KEYWORD articles for keyword extraction
keyword_filename = "data/raw/leapscholar_news_keywords.csv"
with open(keyword_filename, mode="w", encoding="utf-8", newline="") as csv_file:
    fieldnames = ["source_name", "title", "url"]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for article in keyword_articles:
        writer.writerow(article)
print(f"Saved {len(keyword_articles)} KEYWORD news articles to '{keyword_filename}'")

