import yahooquery
import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def get_yahoo_news(symbol,date):
    '''
    :symbol: Stock symbol. String
    :date: date from which news history must be obtained. String
    get all the available news until the specified date. 
    For example if date is 2021-01-29, this returns 
    summary of all news up to 2021-01-29. 
    In general, Yahoo keeps history of only 12 months hence we can only 
    12 months of news
    returns a dataframe with news 
    '''
    assert isinstance(symbol, str)
    assert isinstance(date, str)

    data = []
    run_Dict = []
    ticker = yahooquery.Ticker(symbol)
      
    news = ticker.news(5000,start=date)
    news = pd.DataFrame(news)
    
    news=news[["provider_publish_time","title", "summary"]]
    news = news.sort_values(by=['provider_publish_time'])
    news['date'] = pd.to_datetime(news['provider_publish_time'],unit='s').dt.strftime("%Y-%m-%d")
    news.set_index(pd.to_datetime(news['date']), inplace=True)
    news = news.drop(columns='date')
    return news

def get_sentiment_from_news(news):
    '''
    :news: News data frame
    adds sentiment information to the news data frame
    '''
    assert isinstance(news, pd.DataFrame)
    
    nltk.download("vader_lexicon")
    sentimentAnalyser = SentimentIntensityAnalyzer()

    news["compound"] = [sentimentAnalyser.polarity_scores(v)['compound'] if isinstance(v,str) else v for v in news["summary"]]
    news["negative"] = [sentimentAnalyser.polarity_scores(v)['neg'] if isinstance(v,str) else v for v in news["summary"]]
    news["positive"] = [sentimentAnalyser.polarity_scores(v)['pos'] if isinstance(v,str) else v for v in news["summary"]]
    news["neutral"] = [sentimentAnalyser.polarity_scores(v)['neu'] if isinstance(v,str) else v for v in news["summary"]]

    news_sentiment = news['compound']
    total_sentiment = news_sentiment.groupby('date').agg('sum')
    total_sentiment = total_sentiment.interpolate()
    total_sentiment = total_sentiment.rename('Total Sentiment')
    nArticles = news_sentiment.groupby('date').count()
    avg_sentiment = total_sentiment/nArticles
    avg_sentiment = avg_sentiment.interpolate()
    avg_sentiment = avg_sentiment.rename('Daily average')
    sentiment_data = pd.concat([total_sentiment, avg_sentiment], axis=1)
    sentiment_data['weekly average'] = sentiment_data['Daily average'].rolling(7, win_type='triang').sum()
    sentiment_data['weekly average'] = sentiment_data['weekly average'].interpolate()
    sentiment_data['monthly average'] = sentiment_data['Daily average'].rolling(20, win_type='triang').sum()
    sentiment_data['monthly average'] = sentiment_data['monthly average'].interpolate()
    sentiment_data['long term average'] = sentiment_data['Daily average'].rolling(90, win_type='triang').sum()
    sentiment_data['long term average'] = sentiment_data['long term average'].interpolate()
    return sentiment_data
