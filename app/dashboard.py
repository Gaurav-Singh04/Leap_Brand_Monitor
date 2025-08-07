"""
Streamlit dashboard for Brand Perception Monitor.
"""

import streamlit as st
import pandas as pd
import random
import plotly.express as px

st.set_page_config(page_title="LeapScholar Brand Perception Monitor", layout="wide")

# Load data
twitter_df = pd.read_csv(r"brand_monitor\data\processed\twitter_sentiment.csv")
news_df = pd.read_csv(r"brand_monitor\data\processed\news_sentiment.csv")
try:
    keywords_df = pd.read_csv(r"brand_monitor\data\processed\news_top_keywords.csv")
except Exception:
    keywords_df = pd.DataFrame(columns=["keyword", "frequency"])

st.title("LeapScholar Brand Perception Monitor")
st.markdown("""
<style>
.big-font {font-size:30px !important; font-weight:700;}
.card {background-color: #f6f9fc; border-radius: 10px; padding: 1.5em; margin-bottom: 1em; box-shadow: 0 2px 8px #e3e3e3;}
.sentiment-pos {color: #2ecc40; font-weight: bold;}
.sentiment-neg {color: #e74c3c; font-weight: bold;}
.sentiment-neu {color: #888; font-weight: bold;}
.posts-container {
    background-color: #1e293b;
    border-radius: 12px;
    padding: 1em;
    height: 100%;
    overflow-y: auto;
    max-height: 500px;
    border: 1px solid #334155;
}
.posts-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    text-align: center;
    padding: 0.8rem;
    border-radius: 12px 12px 0 0;
    margin: -1em -1em 1em -1em;
    font-weight: 600;
    font-size: 1rem;
    box-shadow: 0 2px 10px rgba(102, 126, 234, 0.3);
}
.tweet-item, .news-item, .reddit-item {
    background-color: #f8fafc;
    border-radius: 6px;
    padding: 0.8em;
    margin-bottom: 0.8em;
    border-left: 3px solid #3b82f6;
    box-shadow: 0 1px 4px rgba(0,0,0,0.1);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.tweet-item:hover, .news-item:hover, .reddit-item:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
.news-item {
    border-left-color: #ef4444;
}
.reddit-item {
    border-left-color: #8b5cf6;
}
.section-title {
    color: #e2e8f0;
    font-weight: 600;
    margin-bottom: 1rem;
    font-size: 1.1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# --- Combined Sentiment Summary ---
st.header("Overall Sentiment Summary")
col1, col2 = st.columns([2, 3])

with col1:
    # Combine Twitter and News sentiment data
    all_sentiments = pd.concat([twitter_df['sentiment'], news_df['sentiment']], ignore_index=True)
    combined_counts = all_sentiments.value_counts().reindex(['Positive','Negative','Neutral'], fill_value=0)
    
    fig1 = px.pie(values=combined_counts.values, names=combined_counts.index, 
                  color=combined_counts.index,
                  color_discrete_map={"Positive":"#2ecc40","Negative":"#e74c3c","Neutral":"#888"},
                  title="Combined Sentiment Distribution")
    fig1.update_layout(height=500, font=dict(size=16))
    fig1.update_traces(textfont_size=20, textposition='auto')
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown("<div class='posts-container'>", unsafe_allow_html=True)
    st.markdown("<div class='posts-header'>📊 Recent Social Media & News Activity</div>", unsafe_allow_html=True)
    
    # Split this column into three sub-columns for tweets, news, and reddit
    sub_col1, sub_col2, sub_col3 = st.columns(3)
    
    with sub_col1:
        st.markdown("<div class='section-title'>🗨️ Recent Tweets</div>", unsafe_allow_html=True)
        if len(twitter_df) > 0:
            for _, row in twitter_df.sample(n=min(3, len(twitter_df))).iterrows():
                st.markdown(f"""
                <div class='tweet-item'>
                    <p style='font-size: 12px; margin-bottom: 6px; color: #1f2937;'>{row['text'][:100]}...</p>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <span class='sentiment-{row['sentiment'].lower()[:3]}'>{row['sentiment']}</span>
                    </div>
                    <div style='font-size: 10px; color: #6b7280; margin-top: 4px;'>
                        👍 {row.get('like_count', 0)} | 🔁 {row.get('retweet_count', 0)} | 💬 {row.get('reply_count', 0)}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No tweets available.")
    
    with sub_col2:
        st.markdown("<div class='section-title'>📰 Recent News</div>", unsafe_allow_html=True)
        if len(news_df) > 0:
            for _, row in news_df.sample(n=min(3, len(news_df))).iterrows():
                st.markdown(f"""
                <div class='news-item'>
                    <p style='font-size: 12px; margin-bottom: 6px; font-weight: 600; color: #1f2937;'>{row['title'][:70]}...</p>
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <span class='sentiment-{row['sentiment'].lower()[:3]}'>{row['sentiment']}</span>
                        <a href='{row['url']}' target='_blank' style='font-size: 11px; color: #ef4444;'>Read</a>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No news articles available.")
    
    with sub_col3:
        st.markdown("<div class='section-title'>🤖 Reddit Posts</div>", unsafe_allow_html=True)
        # Sample Reddit posts (you can replace this with actual Reddit data)
        sample_reddit = [
            {"title": "Actually good credit cards for International Students? (Zolve vs Sable)", "sentiment": "Negative"},
            {"title": "Has anyone used Leap for studying abroad? How was your experience?", "sentiment": "Neutral"},
            {"title": "LeapScholar helped me get into my dream university!", "sentiment": "Positive"}
        ]
        
        for post in sample_reddit[:3]:
            st.markdown(f"""
            <div class='reddit-item'>
                <p style='font-size: 12px; margin-bottom: 6px; color: #1f2937;'>{post['title'][:70]}...</p>
                <div style='display: flex; justify-content: space-between; align-items: center;'>
                    <span class='sentiment-{post['sentiment'].lower()[:3]}'>{post['sentiment']}</span>
                    <a href='#' target='_blank' style='font-size: 11px; color: #8b5cf6;'>View</a>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# --- Bottom Row: Trending Keywords and Engagement Stats ---
st.header("📈 Analytics Overview")
col3, col4 = st.columns([3, 2])

with col3:
    st.subheader("🔍 Trending Keywords")
    if not keywords_df.empty:
        # Create a more visually appealing chart
        fig3 = px.bar(keywords_df.head(8), x='frequency', y='keyword', 
                      orientation='h',
                      color='frequency', 
                      color_continuous_scale='viridis',
                      title="Top Keywords by Frequency")
        fig3.update_layout(
            height=400,
            yaxis={'tickfont': {'size': 14}, 'title': None},
            xaxis={'title': 'Frequency', 'tickfont': {'size': 12}},
            margin=dict(l=120, r=20, t=50, b=50),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#1f2937')
        )
        fig3.update_traces(hovertemplate='<b>%{y}</b><br>Frequency: %{x}<extra></extra>')
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("No keyword data available.")

with col4:
    st.subheader("📊 Engagement Metrics")
    
    # Engagement stats in a more compact format
    eng_cols = ["like_count", "retweet_count", "reply_count"]
    if all(col in twitter_df.columns for col in eng_cols):
        eng_totals = twitter_df[eng_cols].sum()
        
        # Create two columns for metrics and pie chart
        metric_col1, metric_col2 = st.columns([1, 1])
        
        with metric_col1:
            # Display as metrics cards without fake percentages
            st.metric("Total Likes", f"{eng_totals['like_count']:,}")
            st.metric("Total Retweets", f"{eng_totals['retweet_count']:,}")
            st.metric("Total Replies", f"{eng_totals['reply_count']:,}")
        
        with metric_col2:
            # Add a small donut chart for engagement distribution
            eng_df = pd.DataFrame({
                'Metric': ['Likes', 'Retweets', 'Replies'],
                'Count': [eng_totals['like_count'], eng_totals['retweet_count'], eng_totals['reply_count']]
            })
            
            fig4 = px.pie(eng_df, values='Count', names='Metric', 
                          color_discrete_sequence=['#3b82f6', '#ef4444', '#8b5cf6'],
                          hole=0.4)
            fig4.update_layout(
                height=250,
                margin=dict(t=20, b=20, l=20, r=20),
                showlegend=False
            )
            fig4.update_traces(textposition='inside', textinfo='percent')
            st.plotly_chart(fig4, use_container_width=True)
            
        st.markdown("<p style='text-align: center; color: #64748b; font-size: 0.9rem; margin-top: -10px;'>Engagement Distribution</p>", unsafe_allow_html=True)
    else:
        st.info("No engagement data available.")