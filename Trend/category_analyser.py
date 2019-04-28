import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from tweet_cleaner import TweetCleaner

class CategoryAnalyser:
    def __init__(self, cleaned_file = "./data/cleaned_train_category.csv", cleaner = False):
        self.tweets = []
        self.filelist = ['./data/tech_raw.txt' , './data/sports_raw.txt','./data/fnl_raw.txt',
                         './data/business_raw.txt','./data/politics_raw.txt','./data/ent_raw.txt']
        self.labels = ['Technology','Sports','Finance','Business','Politics','Entertainment']
        self.tcl = TweetCleaner()
        if(cleaner):
            self.cleaned_trainfile_creator()
        self.df = pd.read_csv(cleaned_file, encoding = 'latin-1', header = None)
        self.feature_names = None
        
    def dict_creator(self): 
        for k in range(0, len(self.filelist)):
            my_dict = {}
            self.my_list = self.my_list = open(self.filelist[k], 'r').read().split('\n')
            for i in range(0, len(self.my_list)):
                my_dict["category"] = self.labels[k]
                my_dict["text"] = self.tcl.clean_single_tweet(self.my_list[i], True)
                self.tweets.append(my_dict.copy()) 
        df = pd.DataFrame(self.tweets)
        return df
    
    def test_feature_count(self, test_feature):
        count_word = CountVectorizer(vocabulary = self.feature_names)
        return count_word.fit_transform(test_feature)
    
    def counter_value(self, pred):
        return Counter(pred).most_common()

    def cleaned_trainfile_creator(self): 
        df = self.dict_creator()
        self.tcl.cleaned_file_creator("./data/cleaned_train_category.csv", df.category, df.text)

    def modelling(self):
        count_word = CountVectorizer()
        train_features = count_word.fit_transform(self.df[1])
        train_x, test_x, train_y, test_y = train_test_split(train_features, self.df[0], test_size = 0.2)
        model = MultinomialNB().fit(train_x, train_y)
        self.feature_names = count_word.get_feature_names()
        y_pred = model.predict(test_x)
        print(accuracy_score(y_pred, test_y))
        return model