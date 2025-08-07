import json
import pandas as pd

import csv
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

transformer_model = "cardiffnlp/twitter-roberta-base-sentiment"
transformer_tokenizer = AutoTokenizer.from_pretrained(transformer_model)
transformer_pipeline = pipeline("sentiment-analysis", model=transformer_model, tokenizer=transformer_tokenizer)

# Minimal tweet preprocessing for transformer
def preprocess_tweet(text):
    text = re.sub(r'http\S+|www\.\S+', '<url>', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def score_label(label):
    if label == "POSITIVE":
        return 1
    elif label == "NEGATIVE":
        return -1
    else:
        return 0

def get_sentiment_label(score):
    if score > 0.3:
        return "Positive"
    elif score < -0.3:
        return "Negative"
    else:
        return "Neutral"

def analyze_sentiment(text):
    analyzer = SentimentIntensityAnalyzer()
    score = analyzer.polarity_scores(text)
    compound = score['compound']
    if compound >= 0.05:
        return 'Positive'
    elif compound <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'
    

def reddit_sentiment(input_json, output_csv):
    model_name = "distilbert-base-uncased-finetuned-sst-2-english"
    clf = pipeline("sentiment-analysis", model=model_name)
    with open(input_json, encoding="utf-8") as f:
        posts = json.load(f)

    results = []
    for post in posts:
        post_id = post.get("post_id", "")
        title = post.get("post_title", "")
        body = post.get("post_text", "")
        comments = post.get("comments", [])
        # If comments are dicts, get comment body, else assume list of strings
        if comments and isinstance(comments[0], dict):
            comment_texts = [c.get("body", "") for c in comments[:5]]
        else:
            comment_texts = comments[:5]

        post_text = (title or "") + "\n" + (body or "")
        post_pred = clf(post_text[:512])[0]  # Truncate for model
        post_score = score_label(post_pred["label"])

        comment_scores = []
        for c in comment_texts:
            if c.strip():
                pred = clf(c[:512])[0]
                comment_scores.append(score_label(pred["label"]))
        avg_comment_score = sum(comment_scores)/len(comment_scores) if comment_scores else 0

        overall_score = 0.7 * post_score + 0.3 * avg_comment_score
        sentiment = get_sentiment_label(overall_score)

        results.append({
            "post_id": post_id,
            "title": title,
            "body": body,
            "post_score": post_score,
            "avg_comment_score": avg_comment_score,
            "overall_score": overall_score,
            "sentiment": sentiment,
            "platform": "Reddit"
        })

    df = pd.DataFrame(results)
    df.to_csv(output_csv, index=False)


def sentiment_twitter(input_csv, output_csv):
    label_map = {
        'LABEL_0': 'Negative',
        'LABEL_1': 'Positive',
        'LABEL_2': 'Neutral'
    }
    with open(input_csv, encoding='utf-8') as infile, open(output_csv, 'w', encoding='utf-8', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['sentiment', 'platform']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            new_row = dict(row)
            text = row.get('text', '')
            pre_text = preprocess_tweet(text)
            try:
                hf_result = transformer_pipeline(pre_text)[0]['label']
            except Exception:
                hf_result = ''
            new_row['sentiment'] = label_map.get(hf_result, hf_result)
            new_row['platform'] = 'Twitter'
            writer.writerow(new_row)

def sentiment_news(input_csv, output_csv):
    with open(input_csv, encoding='utf-8') as infile, open(output_csv, 'w', encoding='utf-8', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['sentiment', 'platform']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            new_row = dict(row)
            title = row.get('title', '')
            new_row['sentiment'] = analyze_sentiment(title)
            new_row['platform'] = 'News'
            writer.writerow(new_row)

def main():
    print("Running sentiment analysis for Reddit JSON...")
    reddit_sentiment(
        "data/raw/reddit_leapscholar.json",
        "data/processed/reddit_sentiment.csv"
    )
    print("Reddit sentiment saved to brand_monitor/data/processed/reddit_sentiment.csv")

    print("Running sentiment analysis for Twitter and News CSVs...")
    sentiment_twitter(
        "data/raw/leapscholar_tweets.csv",
        "data/processed/twitter_sentiment.csv"
    )
    print("Twitter sentiment saved to brand_monitor/data/processed/twitter_sentiment.csv")

    print("Running sentiment analysis for News CSVs...")
    sentiment_news(
        "data/raw/leapscholar_news_leap.csv",
        "data/processed/news_sentiment.csv"
    )
    print("News sentiment saved to brand_monitor/data/processed/news_sentiment.csv")

if __name__ == "__main__":
    main()
