# LeapScholar Brand Perception Monitor

A sentiment-driven monitoring dashboard for LeapScholar, built with Streamlit. This solution provides real-time insights into public perception by aggregating and analyzing data from Twitter (X), Reddit, and News sources. It leverages advanced NLP models for sentiment analysis, extracts trending keywords, and visualizes engagement metrics—all in a modern, interactive dashboard.

---

## Features
- **Overall Sentiment Summaries:** Visualizes sentiment (Positive, Neutral, Negative) for each platform.
- **Top 3 Public Mentions:** Displays the most recent tweets, Reddit posts, and news headlines with sentiment labels.
- **Trending Topics:** Extracts and visualizes top keywords from each source to highlight emerging topics.
- **Engagement Statistics:** Shows likes, retweets, and replies over time for Twitter.

---

## Technical Overview

### 1. Data Collection
- **Twitter:** Uses the X (Twitter) API to search for brand-related queries (e.g., "LeapScholar", "LeapScholar review") to maximize relevant results.
- **Reddit:** Utilizes Reddit's API via PRAW to fetch posts and top comments mentioning "LeapScholar" for sentiment and topic analysis.
- **News:** Collects recent headlines mentioning the brand using NewsAPI. Only headlines are analyzed due to limited access to full article content.

### 2. Sentiment Analysis Layer
Each platform's language style is different, so we use domain-appropriate models for best accuracy:
- **Twitter:** [`cardiffnlp/twitter-roberta-base-sentiment`](https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment)
  - Fine-tuned for Twitter's unique language (abbreviations, emojis, informal grammar).
  - Provides tweet-level sentiment with contextual understanding of short social media text.
- **Reddit:** [`distilbert-base-uncased-finetuned-sst-2-english`](https://huggingface.co/distilbert-base-uncased-finetuned-sst-2-english)
  - Effective for longer, more grammatically consistent posts and comments.
  - Delivers robust sentiment classification for general English text.
- **News:** [VADER SentimentIntensityAnalyzer](https://github.com/cjhutto/vaderSentiment)
  - Optimized for short texts and headlines.
  - Fast, interpretable, and accurate for neutral journalistic tone.

All sentiment outputs are normalized to Positive, Neutral, or Negative.

### 3. Keyword Extraction
- **KeyBERT** is used to extract high-quality keywords from tweets, Reddit posts, and news headlines.
- It leverages BERT embeddings to identify semantically important words and phrases, making it ideal for summarizing trending topics and surfacing what matters most in public discourse.

---

## Business Overview
- **Model/Tool Selection:** Each model or tool is chosen for its suitability to the content type, ensuring accurate and actionable results.
- **Modular Architecture:** The system is built in modular parts, making it easy to extend with new data sources or analytics features.
- **Transparent Data Storage:** All data is saved in CSV/JSON formats for easy auditing, dashboard integration, or further analysis.
- **User-Friendly Dashboard:** The Streamlit dashboard is designed for rapid, intuitive insights—supporting both high-level monitoring and deep dives into specific posts or topics.

---

## Tools & Libraries Used
- **Python** (pandas, plotly, streamlit)
- **tweepy** (Twitter API), **PRAW** (Reddit API), **feedparser** (News RSS)
- **transformers** (HuggingFace), **KeyBERT**, **VADER**

---

## Getting Started
1. Clone the repository and install requirements:
   ```bash
   pip install -r requirements.txt
   ```
2. Set up API credentials for Twitter and Reddit in a `.env` file.
3. Run the data collection scripts in `modules/` to fetch and process data.
4. Launch the dashboard:
   ```bash
   streamlit run app/dashboard.py
   ```

---

## Extensibility
- The modular design allows for easy addition of new data sources, analytics, or visualizations as business needs evolve.

---

## License
MIT License
