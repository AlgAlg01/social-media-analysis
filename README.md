# 📊 social-media-analysis

This project analyzes trends and engagement across Reddit and Twitter by categorizing content into sectors like Politics, Education, Technology, Health, and Entertainment. It fetches social media data using platform APIs, evaluates performance metrics, and produces weekly insights with statistical summaries.

---

## 🚀 Features

- 🔍 **Cross-Platform Analysis** (Reddit & Twitter)
- 📊 **Sector rankings by:**
  - *Virality* (reach, shares, upvotes, retweets)
  - *Engagement* (likes, comments, replies)
  - *Engagement Rate* (engagement normalized by post count or audience)
- 📅 **Weekly trend tracking by sector**
- 🧠 **Top 10 trending topics by virality and engagement**
- 📈 **Statistical summaries: mean, median, standard deviation**
- 📚 **Reddit-specific analysis by subreddit**
- 🐦 **Twitter-specific analysis by search query**

# ⚙️ Setup Instructions

This guide will help you install, configure, and run the Social Media Analyzer.

---

## 1. Clone the Repository

```bash
git clone https://github.com/AlgAlg01/social-media-analyzer.git
cd social-media-analyzer
```

## 2. Install dependencies

```bash
pip install -r requirements.txt
```
## 3. Create a .env file
In the root of the proyect, create a .env file with the following content:
```env
REDDIT_CLIENT_ID=placeholder
REDDIT_CLIENT_SECRET=placeholder
REDDIT_USER_AGENT=placeholder
TWITTER_BEARER_TOKEN=placeholder
```
## 4. Run the proyect
Go to main.ipynb, run the first code box and then the 2nd code box. Then you can run the 3rd code box for the Reddit analysis and the 4th code box for the Twitter one
