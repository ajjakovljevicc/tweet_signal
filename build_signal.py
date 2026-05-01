import pandas as pd 

#combine sentiment and daily returns
tweet_sentiment = pd.read_csv('data/tweets_sentiment.csv')
daily_signal = tweet_sentiment.groupby('date')[['sentiment']].mean().reset_index()
daily_returns = tweet_sentiment.groupby('date')[['daily_returns']].mean().reset_index()
sentiment_returns = pd.merge(daily_signal, daily_returns, on='date')

#filter by presidency 
sentiment_returns['date'] = pd.to_datetime(sentiment_returns['date'])
first_presidency = sentiment_returns[
    (sentiment_returns['date'] >= '2017-01-20') &
    (sentiment_returns['date'] <= '2021-01-20')
]

#filter by event


#filter by extreme sentiment
extreme_first = first_presidency[
    (first_presidency['sentiment'] > 0.3) |
    (first_presidency['sentiment'] < -0.3)
]

#current correlation (extreme days)
correlation = extreme_first['sentiment'].corr(extreme_first['daily_returns'])
print(correlation)

#lagged correlation -- forward looking (extreme first)
extreme_first['next_day_returns'] = extreme_first['daily_returns'].shift(-1)
correlation_lagged = extreme_first['sentiment'].corr(extreme_first['next_day_returns'])
print(correlation_lagged)

print(len(extreme_first))