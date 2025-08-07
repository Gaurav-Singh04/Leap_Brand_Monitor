
import json

def extract_reddit_keywords(input_json, output_csv, top_n=15):
    kw_model = KeyBERT()
    with open(input_json, encoding='utf-8') as f:
        posts = json.load(f)
    texts = []
    for post in posts:
        title = post.get('post_title', '')
        body = post.get('post_text', '')
        combined = f"{title}\n{body}".strip()
        if combined:
            texts.append(combined)
    all_keywords = []
    for text in texts:
        keywords = kw_model.extract_keywords(text, top_n=3, stop_words='english')
        all_keywords.extend([kw[0].lower() for kw in keywords])
    counter = Counter(all_keywords)
    top_keywords = counter.most_common(top_n)
    with open(output_csv, 'w', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['keyword', 'frequency'])
        for keyword, freq in top_keywords:
            writer.writerow([keyword, freq])
import csv
from keybert import KeyBERT
from collections import Counter

def extract_top_keywords(input_csv, output_csv, top_n=15):
    kw_model = KeyBERT()
    titles = []
    with open(input_csv, encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            title = row.get('title', '')
            if title:
                titles.append(title)
    all_keywords = []
    for title in titles:
        keywords = kw_model.extract_keywords(title, top_n=3, stop_words='english')
        all_keywords.extend([kw[0].lower() for kw in keywords])
    counter = Counter(all_keywords)
    top_keywords = counter.most_common(top_n)
    with open(output_csv, 'w', encoding='utf-8', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(['keyword', 'frequency'])
        for keyword, freq in top_keywords:
            writer.writerow([keyword, freq])


if __name__ == "__main__":
    print("Extracting top keywords from news articles...")
    extract_top_keywords(
        "brand_monitor/data/raw/leapscholar_news_keywords.csv",
        "brand_monitor/data/processed/news_top_keywords.csv"
    )
    print("Top keywords saved to brand_monitor/data/processed/news_top_keywords.csv")

    print("Extracting top keywords from reddit posts...")
    extract_reddit_keywords(
        "brand_monitor/data/raw/reddit_leapscholar.json",
        "brand_monitor/data/processed/reddit_top_keywords.csv"
    )
    print("Top keywords saved to brand_monitor/data/processed/reddit_top_keywords.csv")