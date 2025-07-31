import praw
import pandas as pd
from datetime import datetime


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