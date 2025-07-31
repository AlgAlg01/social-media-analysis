import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class RedditSocialMediaAnalyzer:
    def __init__(self, df):
        """Initialize with real data"""
        self.df = df
        self.preprocess_data()
    
    def preprocess_data(self):
        """Clean and prepare data for analysis"""
        # Convert date to datetime
        self.df['date'] = pd.to_datetime(self.df['date'])
        
        # Create time-based features
        self.df['week'] = self.df['date'].dt.to_period('W')
        self.df['month'] = self.df['date'].dt.to_period('M')
        
        # Calculate virality score... We have no views, if we had them virality=views
        self.df['virality'] = self.df['engagement'] + (self.df['shares'] * 2)
        
        #Engagement for each subreddit subscriber... Again, more accurate if we hade views
        self.df['engagement_rate'] = self.df['engagement']/self.df['subreddit_subs']
    
    def analyze_sector_performance(self):
        """Analyze and visualize performance by sector"""
        sector_stats = self.df.groupby('sector').agg({
            'virality': 'mean',
            'engagement': 'mean',
            'engagement_rate': 'mean'
        }).reset_index()
        
        # Virality by Sector
        plt.figure(figsize=(12, 6))
        sns.barplot(data=sector_stats.sort_values('virality', ascending=False), 
                    x='sector', y='virality', palette='viridis', hue='x', legend=False)
        plt.title('Average Virality Score by Sector')
        plt.ylabel('Virality Score')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
        
        #Engagement
        plt.figure(figsize=(12, 6))
        sns.barplot(data=sector_stats.sort_values('engagement', ascending=False), 
                    x='sector', y='engagement', palette='plasma',hue='x',legend=False)
        plt.title('Average Engagement by Sector')
        plt.ylabel('Engagement')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
        
        # Engagement Rate by Sector
        plt.figure(figsize=(12, 6))
        sns.barplot(data=sector_stats.sort_values('engagement_rate', ascending=False), 
                    x='sector', y='engagement_rate', palette='magma',hue='x',legend=False)
        plt.title('Average Engagement Rate by Sector')
        plt.ylabel('Engagement Rate')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
    
    def analyze_topic_performance(self):
        """Analyze and visualize performance by topic within sectors"""
        topic_stats = self.df.groupby(['sector', 'topic']).agg({
            'virality': 'mean',
            'engagement': 'mean'
        }).reset_index()
        
        # Top topics by virality
        top_viral = topic_stats.sort_values('virality', ascending=False).head(10)
        plt.figure(figsize=(12, 8))
        sns.barplot(data=top_viral, x='virality', y='topic', hue='sector', dodge=False)
        plt.title('Top 10 Most Viral Topics')
        plt.xlabel('Virality Score')
        plt.ylabel('Topic')
        plt.legend(title='Sector', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.show()
        
        # Top topics by engagement
        top_retention = topic_stats.sort_values('engagement', ascending=False).head(10)
        plt.figure(figsize=(12, 8))
        sns.barplot(data=top_retention, x='engagement', y='topic', hue='sector', dodge=False)
        plt.title('Top 10 Topics with Highest Engagement')
        plt.xlabel('Engagement')
        plt.ylabel('Topic')
        plt.legend(title='Sector', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.show()
    
    def analyze_trends(self):
        """Analyze trends over time"""
        # Weekly virality trends by sector
        weekly_trends = self.df.groupby(['week', 'sector'])['virality'].mean().reset_index()
        weekly_trends['week'] = weekly_trends['week'].dt.to_timestamp()
        
        plt.figure(figsize=(14, 7))
        sns.lineplot(data=weekly_trends, x='week', y='virality', hue='sector', marker='o')
        plt.title('Weekly Virality Trends by Sector')
        plt.ylabel('Average Virality')
        plt.xlabel('Week')
        plt.xticks(rotation=45)
        plt.legend(title='Sector', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.show()
        
        # Monthly engagement trends by sector
        monthly_trends = self.df.groupby(['month', 'sector'])['engagement'].mean().reset_index()
        monthly_trends['month'] = monthly_trends['month'].dt.to_timestamp()
        
        plt.figure(figsize=(14, 7))
        sns.lineplot(data=monthly_trends, x='month', y='engagement', hue='sector', marker='o')
        plt.title('Monthly Engagement Trends by Sector')
        plt.ylabel('Average Engagement')
        plt.xlabel('Month')
        plt.xticks(rotation=45)
        plt.legend(title='Sector', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        plt.show()
    
    def generate_report(self):
        """Generate comprehensive analysis report"""
        print("=== Reddit Performance Analysis ===\n")
        
        # Sector summary
        sector_summary = self.df.groupby('sector').agg({
            'virality': ['mean', 'median', 'std'],
            'engagement': ['mean', 'median', 'std'],
            'post_id': 'count'
        }).round(2)
        print("Sector Performance Summary:")
        print(sector_summary)
        print("\n")
        
        # Top performing subreddits
        subreddit_stats = self.df.groupby(['sector', 'subreddit']).agg({
            'virality': 'mean',
            'engagement': 'mean'
        }).sort_values(['sector', 'virality'], ascending=[True, False])
        
        print("Top Performing Subreddits by Sector:")
        for sector in subreddit_stats.index.get_level_values(0).unique():
            print(f"\n{sector}:")
            print(subreddit_stats.loc[sector].head(2))
        
        print("\n=== Analysis Complete ===")
