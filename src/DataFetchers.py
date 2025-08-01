import praw
import pandas as pd
from datetime import datetime
import tweepy

class RedditDataFetcher:
    def __init__(self, client_id, client_secret, user_agent):
        """Initialize Reddit API client"""
        self.reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )
        
    def fetch_posts(self, subreddits, time_filter='month', limit=100):
        """Fetch top posts from specified subreddits"""
        all_posts = []
        
        for sector, subs in subreddits.items():
            for sub in subs:
                try:
                    subreddit = self.reddit.subreddit(sub)
                    top_posts = subreddit.top(time_filter=time_filter, limit=limit)
                    subreddit_subscribers = subreddit.subscribers
                    
                    for post in top_posts:
                        # Calculate engagement metrics
                        engagement = post.score + post.num_comments
                        shares = post.num_crossposts  # Crossposts as shares
                        
                        # Create post record
                        record = {
                            'post_id': post.id,
                            'sector': sector,
                            'topic': post.title[:50] + '...',  # Truncated title as topic
                            'engagement': engagement,
                            'shares': shares,
                            'date': datetime.fromtimestamp(post.created_utc),
                            'score': post.score,
                            'comments': post.num_comments,
                            'upvote_ratio': post.upvote_ratio,
                            'subreddit': sub,
                            'subreddit_subs': subreddit_subscribers
                        }
                        all_posts.append(record)
                            
                except Exception as e:
                    print(f"Error fetching posts from r/{sub}: {e}")
                    continue
        
        return pd.DataFrame(all_posts)
    
class TwitterDataFetcher:
    def __init__(self, bearer_token):
        """Initialize Twitter API client"""
        self.client = tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)
        
    def fetch_tweets(self, targets, max_results=100):
        """
        Fetch recent tweets or author tweets for specified targets.
        """
        all_tweets = []
        
        for sector, keywords in targets.items():
            for keyword in keywords:
                query = ''
                if keyword.startswith('@'):
                    # Fetch tweets from user timeline by username
                    username = keyword[1:]
                    try:
                        user = self.client.get_user(username=username)
                        user_id = user.data.id
                        tweets = self.client.get_users_tweets(
                            id=user_id, max_results=max_results,
                            tweet_fields=['created_at', 'public_metrics', 'text']
                        )
                    except Exception as e:
                        print(f"Error fetching tweets from user {username}: {e}")
                        continue
                else:
                    query = f"{keyword}"
                    try:
                        tweets = self.client.search_recent_tweets(
                            query=query, max_results=max_results,
                            tweet_fields=['created_at', 'public_metrics', 'text']
                        )
                    except Exception as e:
                        print(f"Error fetching tweets for keyword {keyword}: {e}")
                        continue
                
                if not tweets or not tweets.data:
                    continue
                
                for tweet in tweets.data:
                    metrics = tweet.public_metrics
                    record = {
                        'tweet_id': tweet.id,
                        'sector': sector,
                        'topic': tweet.text[:50] + '...' if len(tweet.text) > 50 else tweet.text,
                        #'views': tweet.non_public_metrics['impressions']
                        'engagement': metrics['like_count'] + metrics['reply_count'],
                        'likes': metrics['like_count'],
                        'retweets': metrics['retweet_count'],
                        'replies': metrics['reply_count'],
                        'date': tweet.created_at,
                        'text': tweet.text,
                        'target': keyword
                    }
                    all_tweets.append(record)
        
        return pd.DataFrame(all_tweets)   