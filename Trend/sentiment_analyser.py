import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.model_selection import train_test_split 
import nltk
from tweet_cleaner import TweetCleaner
nltk.download("stopwords")

class SentimentAnalysis:
    def __init__(self, file_name = "./data/cleaned_train_sentiment.csv", clean_required = False):
        self.tcl = TweetCleaner()
        if(clean_required):
            self.cleaned_train_file("./data/train.csv")
        self.cleaned_train_tweets = pd.read_csv(file_name, encoding = 'latin-1', header = None)
        self.max_features = 2000
        self.feature_names = None
        self.Classifiers = [
                LogisticRegression(C=0.000000001,solver='liblinear',max_iter=200),
                DecisionTreeClassifier(),
                RandomForestClassifier(n_estimators=30),
                AdaBoostClassifier(),
                MultinomialNB()]
    
    def set_max_features(self, value):
        self.max_features = value
        
    def analyser(self):
        count_word = TfidfVectorizer(max_features = self.max_features, analyzer = "word")
        train_features = count_word.fit_transform(self.cleaned_train_tweets[1].values.astype('U').tolist())
        self.feature_names = count_word.get_feature_names()
        return self.modelling(train_features)
    
    def count_test_feature(self, testfeature):
        count_word2 = TfidfVectorizer(vocabulary = self.feature_names, analyzer = "word")
        test_feature = count_word2.fit_transform(testfeature)
        return test_feature
    
    def best_model(self, model_list):
        return sorted(model_list)[0][1]
    
    def modelling(self, train_f, run_all_classifiers = False):
        model_list = []
        train_x, test_x, train_y, test_y = train_test_split(train_f, self.cleaned_train_tweets[0], test_size = 0.2)
        
        if(not run_all_classifiers):
            self.Classifiers = [MultinomialNB()]
            
        for classifier in self.Classifiers:  
            model = classifier.fit(train_x, train_y)
            pred = model.predict(test_x)
            
            #Evaluation
            accur = accuracy_score(pred, test_y)
            print('Accuracy of '+ classifier.__class__.__name__+' is '+str(accur))   
            model_list.append((accur, model)) 
            
        return self.best_model(model_list)
    
    def cleaned_train_file(self, file_name):
        train_tweets = pd.read_csv(file_name, encoding = 'latin-1')
        train_tweet_list = self.tcl.clean_tweets(train_tweets.SentimentText, False) # clean tweets from entire file
        self.tcl.cleaned_file_creator("./data/cleaned_train_sentiment.csv", train_tweets.Sentiment, train_tweet_list)