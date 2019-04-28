from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
from tweet_cleaner import TweetCleaner
import csv
import twitter_credentials

class TweetRetriever:
    def __init__(self):
        self.top_ten = []
        self.files_csv = ['./data/T1.csv', './data/T2.csv','./data/T3.csv',
                          './data/T4.csv','./data/T5.csv','./data/T6.csv',
                          './data/T7.csv','./data/T8.csv','./data/T9.csv',
                          './data/T10.csv']
        self.auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET_KEY)
        self.auth.set_access_token(twitter_credentials.ACCCESS_KEY, twitter_credentials.ACCESS_SECRET_KEY)
        self.api = API(self.auth, wait_on_rate_limit=True)

    def authentication(self):
        trends = self.api.trends_place(23424848)
        return trends
    
    def trending_topics(self):
        trends = self.authentication()
        data = trends[0]
        trends = data['trends']
        names = [trend['name'] for trend in trends]
        top_ten = names[:10]
        return top_ten
    
    def trending_tweets_file(self):
        for topic, file in zip(self.trending_topics(), self.files_csv):
            tcl = TweetCleaner()
            csvFile = open(file, 'w+')
            csvWriter = csv.writer(csvFile)
            for tweet in Cursor(self.api.search,q=topic,lang="en").items(200):
                cleaned_tweet = tcl.clean_single_tweet(tweet.text)
                csvWriter.writerow([cleaned_tweet])
            csvFile.close()
        