from flask import Flask,render_template,request
import os
import sys,tweepy,csv,re
from textblob import TextBlob
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import pandas as pd 

import urllib.request
import  urllib.parse
#import shutil


app = Flask(__name__)



def percentage(part, whole):
        temp = 100 * float(part) / float(whole)
        return format(temp, '.2f')

def limits(hashtag,tweet_count):
    consumerKey = 'eFTyjI2bsBS822C7gzZyEhnjQ'
    consumerSecret = 'mLR0idkPLzfio5ZfUmqhwXXFWezOWCzRnNayLseZ11OnlTniV4'
    accessToken = '1110564533821558785-6tXEzAw5JbZWRRK98QKOjfavphoiZw'
    accessTokenSecret = 'rYcCU8md8ngfscaerF2Ri25UXJf2McVd6f7Vn03xhpz1g'
    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(accessToken, accessTokenSecret)
    api = tweepy.API(auth)
    searchTerm = str(hashtag)
    NoOfTerms = int(tweet_count)
    tweets = tweepy.Cursor(api.search, q=searchTerm, lang = "en").items(NoOfTerms)
    return tweets

def tweetment(hashtag,tweet_count):

            
    tweets=limits(hashtag,tweet_count)
    searchTerm = str(hashtag)
    NoOfTerms = int(tweet_count)
    print(searchTerm)
    print(NoOfTerms)
        

    print("ANALYSING...............................................................!!!!!!")
    print(searchTerm)
    print(NoOfTerms)
    #print(len([tweets]))

    polarity = 0
    positive = 0
    wpositive = 0
    spositive = 0
    negative = 0
    wnegative = 0
    snegative = 0
    neutral = 0

    count1=0
    all_words=[]
    for tweet in tweets:
        text = tweet.text
        text = text.replace("RT", " ")
        #text = " ".join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())

        print("Tweet: " +text)
        all_words = ' '.join([text])
        data = urllib.parse.urlencode({"text": text})
        u= urllib.request.urlopen("http://text-processing.com/api/sentiment/", data.encode())
        res1 = u.read().decode()
        res2="Sentiment: " + eval(res1)['label']
        res3="_"*40
        
        count1+=1
        print("count-------------------------------------------------------->",count1)
        #Append to temp so that we can store in csv later. I use encode UTF-8
        #tweetText.append(cleanTweet(tweet.text).encode('utf-8'))
        # print (tweet.text.translate(non_bmp_map))    #print tweet's text
        analysis = TextBlob(tweet.text)
        polarity += analysis.sentiment.polarity
        #print(analysis.sentiment.polarity)
        
        
        if (analysis.sentiment.polarity == 0):  # adding reaction of how people are reacting to find average later
            neutral += 1
            print(analysis.sentiment.polarity,"neutral")
        elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 0.3):
            wpositive += 1
        elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 0.6):
            positive += 1
            print(analysis.sentiment.polarity,"positive")
        elif (analysis.sentiment.polarity > 0.6 and analysis.sentiment.polarity <= 1):
            spositive += 1
            print(analysis.sentiment.polarity,"spositive")
        elif (analysis.sentiment.polarity > -0.3 and analysis.sentiment.polarity <= 0):
            wnegative += 1
        elif (analysis.sentiment.polarity > -0.6 and analysis.sentiment.polarity < 0):
            negative += 1
            print(analysis.sentiment.polarity,"negative")
        elif (analysis.sentiment.polarity >= -1 and analysis.sentiment.polarity <= -0.6):
            snegative += 1
            print(analysis.sentiment.polarity,"snegative")

            

    positive = percentage(positive, NoOfTerms)
    wpositive = percentage(wpositive, NoOfTerms)
    spositive = percentage(spositive, NoOfTerms)
    negative = percentage(negative, NoOfTerms)
    wnegative = percentage(wnegative, NoOfTerms)
    snegative = percentage(snegative, NoOfTerms)
    neutral = percentage(neutral, NoOfTerms)

    # finding average reaction
    polarity = polarity / NoOfTerms


    if (polarity == 0):
        gp="Neutral"
    elif (polarity > 0 and polarity <= 0.3):
        gp="Weakly Positive"
    elif (polarity > 0 and polarity <= 0.6):
        gp="Positive"
    elif (polarity > 0.6 and polarity <= 1):
       gp="Strongly Positive"
    elif (polarity > -0.3 and polarity <= 0):
       gp="Weakly Negative"
    elif (polarity > -0.6 and polarity < 0):
       gp="Negative"
    elif (polarity >= -1 and polarity <= -0.6):
       gp="Strongly Negative"

    labels = ['Positive [' + str(positive) + '%]','Strongly Positive [' + str(spositive) + '%]', 'Strongly Negative [' + str(snegative) + '%]', 'Neutral [' + str(neutral) + '%]','Negative [' + str(negative) + '%]','Weakly Negative [' + str(wnegative) + '%]','Weakly Positive [' + str(wpositive) + '%]' ]
    sizes = [positive, spositive,snegative, neutral, negative ,wnegative,wpositive]
    colors = ['#64dd17','#1b5e20','#d50000', '#ffff00', 'red','orange','#43b84d']

    #dir_name = "__pycache__"
    #if os.path.isdir(dir_name):
        #shutil.rmtree('__pycache__')
    
    # only "explode" the 2nd slice (i.e. 'Hogs')
    explode = (0.0, 0.0, 0.0, 0.0,0.0,0.0,0.0)

    #add colors
    #colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99']

    #explode = (0.04,0.1,0.04,0.04,0.1)
    plt.figure()
    plt.pie(sizes, colors = colors, startangle=90, pctdistance=0.85, explode = explode)
    patches, texts = plt.pie(sizes, colors=colors, startangle=90)
    plt.legend(patches, labels,loc="lower right",bbox_to_anchor=(1.05, 0.5),fontsize='small')
    #draw circle
    centre_circle = plt.Circle((0,0),0.60)
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    # Equal aspect ratio ensures that pie is drawn as a circle
    plt.axis('equal')  
    files= os.listdir('static/img/')
    if 'result.png' in files:
        os.remove('static/img/result.png')
    fig2 = plt.gcf()
    #plt.show()
    fig2.savefig('static/img/result.png',bbox_inches="tight",dpi=400,transparent=True)

    files= os.listdir('static/img/')
    if 'result12.png' in files:
        os.remove('static/img/result12.png')
    
    stopwords = set(STOPWORDS)
    wordcloud = WordCloud(width = 800, height = 500, background_color ='white', stopwords = stopwords, min_font_size = 3).generate(all_words)
  
    # plot the WordCloud image
    plt.figure()
    plt.figure(figsize = (50, 30), facecolor = 'k') 
    plt.imshow(wordcloud) 
    plt.axis("off") 
    #plt.tight_layout(pad = 0) 
  
    plt.savefig('static/img/result12.png',bbox_inches="tight",dpi=400,transparent=True)
        
        
    results=[searchTerm,NoOfTerms,gp]


    
    return results

def analyse(tweet):
    data = []
    text = tweet.text
    #print("Tweet: " +text)
    text = text.replace("RT", " ")
    #print(dir(tweet))
    msg = "Language : " + tweet.lang
    data.append(msg)
   
    #text = " ".join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())
    msg = "Tweet : " + text
    data.append(msg)
    analysis = TextBlob(text)
    # print(analysis.sentiment)
    if analysis.sentiment.polarity == 0:
        msg = "Sentiment : Neutral"
    elif analysis.sentiment.polarity > 0:
        msg = "Sentiment : Positive"
    else:
        msg = "Sentiment : Negative"
    data.append(msg)
    return data


#home() serves the home page(i.e index.html

@app.route('/')

def home():
    return render_template("index.html")


@app.route("/result",methods = ['POST'])

def analyize():
    if request.method == "POST":
        hashtag = request.form["hashtag"]
        tweet_count = request.form["tweet_count"]
    print(hashtag)
    print(tweet_count)
    res=tweetment(hashtag,tweet_count)
    return render_template("result.html",limits=limits,results=res,analyse=analyse,hashtag=hashtag, tweet_count=tweet_count)

if __name__ == '__main__':
    app.run(debug=True)
