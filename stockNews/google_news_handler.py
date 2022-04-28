# import pandas as pd
# from newspaper import Config
# from GoogleNews import GoogleNews
import datetime
from dataclasses import dataclass

from pygooglenews import GoogleNews
from yfinance.ticker import TickerBase


@dataclass
class News:
    title: str
    link: str


class GoogleNewsHandler:
    _googlenews = None
    # _yfinancenews = None
    _ticker_news_map = {}

    # _config = None

    @staticmethod
    def __initialise():
        if GoogleNewsHandler._googlenews is None:
            GoogleNewsHandler._googlenews = GoogleNews(country='IN')

            # GoogleNewsHandler._yfinancenews = yfinance.ticker.TickerBase.get_news()
            # GoogleNewsHandler._config = Config()

            # user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'
            # GoogleNewsHandler._config.browser_user_agent = user_agent
            # GoogleNewsHandler._config.request_timeout = 20
        # GoogleNewsHandler._googlenews.clear()
        return GoogleNewsHandler._googlenews

    @staticmethod
    def get_headlines(ticker=None, past_days=30, max_news_count=50):
        googlenews = GoogleNewsHandler.__initialise()
        to_date = datetime.datetime.now()
        from_date = to_date - datetime.timedelta(days=past_days)
        date_format = "%Y-%m-%d"
        # googlenews.set_period(f"{past_days}d")

        if GoogleNewsHandler._ticker_news_map.get(ticker) is None:
            gn = googlenews.search(query=f"intitle:{ticker}", from_=from_date.strftime(date_format), to_=to_date.strftime(date_format))
            ticker_news = []
            for news in gn['entries']:
                ticker_news.append(News(news['title'], news['link']))

            # googlenews.get_news(f"{ticker}")
            # googlenews.search(f"{ticker}")
            # result = googlenews.results()
            # # store the results
            # df = pd.DataFrame(result)
            GoogleNewsHandler._ticker_news_map[ticker] = ticker_news

        return GoogleNewsHandler._ticker_news_map[ticker][:max_news_count]

    @staticmethod
    def get_article(ticker=None, index=0):
        """
        Defaults to past_days and max_news_count as defined by the user while getting headlines. User should send the
        index of the news article to get from list of headlines.
        """
        if GoogleNewsHandler._ticker_news_map.get(ticker) is None:
            GoogleNewsHandler.get_headlines(ticker=ticker)

        df = GoogleNewsHandler._ticker_news_map[ticker]
        gnews_link = df['link'][index]
        return f"https://{gnews_link}"


if __name__ == "__main__":
    stock_tickers = {"ASIANPAINT": "ASIAN PAINTS",
                     "ATGL": "ADANI ENTERPRISES",
                     "ADANIGREEN": "ADANI GREEN ENERGY",
                     "ADANIENT": "ADANI ENTERPRISES",
                     "BAJFINANCE": "BAJAJ FINANCE"}

    headlines = GoogleNewsHandler.get_headlines(ticker="ADANI GREEN", past_days=30, max_news_count=10)
    articles = GoogleNewsHandler.get_article(ticker="ADANI GREEN")
    print("done")

'''
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from GoogleNews import GoogleNews
from newspaper import Article
from newspaper import Config
from wordcloud import WordCloud, STOPWORDS

nltk.download('vader_lexicon') #required for Sentiment Analysis

now = dt.date.today()
now = now.strftime('%m-%d-%Y')
yesterday = dt.date.today() - dt.timedelta(days = 30)
yesterday = yesterday.strftime('%m-%d-%Y')

nltk.download('punkt')
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0'
config = Config()
config.browser_user_agent = user_agent
config.request_timeout = 20

# save the company name in a variable
company_name = input("Please provide the name of the Company or a Ticker: ")
#As long as the company name is valid, not empty...
if company_name != '':
    print(f'Searching for and analyzing {company_name}, Please be patient, it might take a while...')

    #Extract News with Google News
    googlenews = GoogleNews(start=yesterday,end=now)
    googlenews.search(company_name)
    result = googlenews.results()
    #store the results
    df = pd.DataFrame(result)
    print(df)

try:
    list =[] #creating an empty list
    for i in df.index:
        dict = {} #creating an empty dictionary to append an article in every single iteration
        article = Article(df['link'][i],config=config) #providing the link
        try:
          article.download() #downloading the article
          article.parse() #parsing the article
          article.nlp() #performing natural language processing (nlp)
        except Exception as e:
            print(e)
            pass
        #storing results in our empty dictionary
        dict['Date']=df['date'][i]
        dict['Media']=df['media'][i]
        dict['Title']=article.title
        dict['Article']=article.text
        dict['Summary']=article.summary
        dict['Key_words']=article.keywords
        list.append(dict)
    check_empty = not any(list)
    # print(check_empty)
    if check_empty == False:
      news_df=pd.DataFrame(list) #creating dataframe
      print(news_df)

except Exception as e:
    #exception handling
    print("exception occurred:" + str(e))
    print('Looks like, there is some error in retrieving the data, Please try again or try with a different ticker.' )

#Sentiment Analysis
def percentage(part,whole):
    return 100 * float(part)/float(whole)

#Assigning Initial Values
positive = 0
negative = 0
neutral = 0
#Creating empty lists
news_list = []
neutral_list = []
negative_list = []
positive_list = []

#Iterating over the tweets in the dataframe
for news in news_df['Summary']:
    news_list.append(news)
    analyzer = SentimentIntensityAnalyzer().polarity_scores(news)
    neg = analyzer['neg']
    neu = analyzer['neu']
    pos = analyzer['pos']
    comp = analyzer['compound']

    if neg > pos:
        negative_list.append(news) #appending the news that satisfies this condition
        negative += 1 #increasing the count by 1
    elif pos > neg:
        positive_list.append(news) #appending the news that satisfies this condition
        positive += 1 #increasing the count by 1
    elif pos == neg:
        neutral_list.append(news) #appending the news that satisfies this condition
        neutral += 1 #increasing the count by 1

positive = percentage(positive, len(news_df)) #percentage is the function defined above
negative = percentage(negative, len(news_df))
neutral = percentage(neutral, len(news_df))

#Converting lists to pandas dataframe
news_list = pd.DataFrame(news_list)
neutral_list = pd.DataFrame(neutral_list)
negative_list = pd.DataFrame(negative_list)
positive_list = pd.DataFrame(positive_list)
#using len(length) function for counting
print("Positive Sentiment:", '%.2f' % len(positive_list), end='\n')
print("Neutral Sentiment:", '%.2f' % len(neutral_list), end='\n')
print("Negative Sentiment:", '%.2f' % len(negative_list), end='\n')

#Creating PieCart
labels = ['Positive ['+str(round(positive))+'%]' , 'Neutral ['+str(round(neutral))+'%]','Negative ['+str(round(negative))+'%]']
sizes = [positive, neutral, negative]
colors = ['yellowgreen', 'blue','red']
patches, texts = plt.pie(sizes,colors=colors, startangle=90)
plt.style.use('default')
plt.legend(labels)
plt.title("Sentiment Analysis Result for stock= "+company_name+"" )
plt.axis('equal')
plt.show()

# Word cloud visualization
def word_cloud(text):
    stopwords = set(STOPWORDS)
    allWords = ' '.join([nws for nws in text])
    wordCloud = WordCloud(background_color='black',width = 1600, height = 800,stopwords = stopwords,min_font_size = 20,max_font_size=150,colormap='prism').generate(allWords)
    fig, ax = plt.subplots(figsize=(20,10), facecolor='k')
    plt.imshow(wordCloud)
    ax.axis("off")
    fig.tight_layout(pad=0)
    plt.show()

print('Wordcloud for ' + company_name)
word_cloud(news_df['Summary'].values)

'''
