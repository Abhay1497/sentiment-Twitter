from twitter_retr import TweetRetriever
from category_analyser import CategoryAnalyser
from sentiment_analyser import SentimentAnalysis
import pandas as pd

class TwitterBokehInteractor:
    def __init__(self):
        self.sentiment_analysis = SentimentAnalysis()
        self.sentiment_analysis_model = self.sentiment_analysis.analyser()
        self.category_analysis = CategoryAnalyser()
        self.category_analysis_model = self.category_analysis.modelling()
        self.twitter_api_obj = TweetRetriever()
        self.twitter_api_obj.trending_tweets_file()
        
    def sentiment_array(self, trend_number):
        data = pd.read_csv("./data/T" + str(trend_number) + ".csv", header = None)
        test_feature = self.sentiment_analysis.count_test_feature(data[0])
        value = []
        for i in range(2, test_feature.shape[0] - 1, 25):
            pred = self.sentiment_analysis_model.predict(test_feature[:i, :])
            value.append(sum(pred)/ len(pred))
        return value

    def trending_topics(self):
        return self.twitter_api_obj.trending_topics()
    
    def countplot(self, trend_number):
        data = pd.read_csv("./data/T" + str(trend_number) + ".csv", header = None)
        test_feature = self.category_analysis.test_feature_count(data[0])
        pred = self.category_analysis_model.predict(test_feature)
        value = self.category_analysis.counter_value(pred)
        return value
    
    def word_cloud_words(self, trend_number):
        data = pd.read_csv("./data/T" + str(trend_number) + ".csv", header = None)
        return " ".join(data[0])
