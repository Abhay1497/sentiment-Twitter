from twitter_bokeh_interactor import TwitterBokehInteractor
from bokeh.models.widgets import Panel, Tabs
from bokeh.plotting import figure
from bokeh.layouts import layout
from bokeh.layouts import row,column
from bokeh.io import save, output_file
from bokeh.models import Range1d, PanTool, ResetTool
from wordcloud import WordCloud, STOPWORDS
import nltk
from bokeh.palettes import Spectral6
from bokeh.models import ColumnDataSource
from bokeh.transform import factor_cmap
import matplotlib.pyplot as plt

def wordcloud(tweets,col):
    nltk.download("stopwords")
    stopwords = set(STOPWORDS)
    wordcloud = WordCloud(background_color="white",stopwords=stopwords,random_state = 2016).generate(tweets)
    plt.figure(figsize=(50,30), facecolor='k')
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.title("WordCloud")
    plt.savefig('./images/a'+col+'.png') 
    p = figure(x_range=(0,1), y_range=(0,1))
    p.image_url(url=['./images/a'+col+'.png'], x=0, y=1, h=1, w=1)
    p.xaxis.visible= False
    p.yaxis.visible= False    
    return p

def call_Sentimentplot(s):
    a=[25,50,75,100,125,150,175,200]   #Convert dataframe into list range list 
    i=0
    pos= s 
    pos = [j*100 for j in pos]
    neg=[]
    for i in range(len(a)):     
        neg.append(100-pos[i])     
    fig = figure() 
    fig.width=600
    fig.height=300
    fig.background_fill_color='azure'
    fig.background_fill_alpha=0.2

    #Style the title
    fig.title.text="Sentiment on Trending Tweets"
    fig.title.text_color="olive"
    fig.title.text_font="times"
    fig.title.text_font_size="25px"
    fig.title.align="center"

        
    #Style the axes
    fig.xaxis.minor_tick_line_color="blue"
    fig.yaxis.major_label_orientation="vertical"
    fig.xaxis.visible=True
    fig.xaxis.minor_tick_in=-6
    fig.xaxis.axis_label="Number of Trending Tweets "
    fig.yaxis.axis_label="Percentage(%)"
    fig.axis.axis_label_text_color="blue"
    fig.axis.major_label_text_color="orange"

    #Axes geometry
    fig.y_range = Range1d(start=0, end=100)

    #Style the grid
    fig.xgrid.grid_line_color = None
    fig.ygrid.grid_line_alpha = 0.3
    fig.grid.grid_line_dash = [5,3]

    #adding glyph:
    fig.line(x=a,y=pos,color='red',legend='Positive Sentiment Trend')
    fig.line(x=a,y=neg,color='blue',legend='Negative Sentiment Trend')
    
    #Style the legend
    fig.legend.location = 'top_right'
    fig.legend.background_fill_alpha = 0.8
    fig.legend.border_line_color = None
    fig.legend.padding = 18
    fig.legend.label_text_color = 'olive'
    fig.legend.label_text_font = 'times'

    #Style the tools
    fig.tools = [PanTool(),ResetTool()]
    fig.toolbar_location = 'above'
    fig.toolbar.logo = None  
    return(fig)  

def Categorical_plot(c):
    c=dict(c)
    category = list(c.keys())
    counts = list(c.values())
    source = ColumnDataSource(data=dict(category=category, counts=counts))
    p = figure(x_range=category,plot_height=300, toolbar_location=None, title="Category")
    p.vbar(x='category', top='counts', width=0.8,source=source, legend="category",
       line_color='white', fill_color=factor_cmap('category', palette=Spectral6, factors=category))

    p.xgrid.grid_line_color = None
    p.legend.orientation = "horizontal"
    p.legend.location = "top_center"
    return p    

def callDashboard():
    l=["1","2","3","4","5","6","7","8","9","10"]
    TwitterBokehInteractor_Object=TwitterBokehInteractor()
    Trendingtopic=TwitterBokehInteractor_Object.trending_topics()
    objectList=[]
    for i in range(len(l)):
        print("1 Done")
        objectList.append(Panel(child=row(
                column(call_Sentimentplot(TwitterBokehInteractor_Object.sentiment_array(l[i])),
                Categorical_plot(TwitterBokehInteractor_Object.countplot(l[i]))),
                wordcloud(TwitterBokehInteractor_Object.word_cloud_words(l[i]),l[i])) , title=Trendingtopic[i] , ))
    tabs = Tabs(tabs=[t for t in objectList ])
    BigPanel = Panel(child=tabs, title="Ongoing_Trend/Hashtag " )
    tabs1 = Tabs(tabs=[BigPanel])
    lay_out1=layout([[tabs1]],sizing_mode='stretch_both')
    print("Return")
    return lay_out1
    

layout_web=callDashboard()
output_file("WEB_OUTPUT.html")
save(layout_web)