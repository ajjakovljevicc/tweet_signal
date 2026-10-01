import pandas as pd 
import numpy as np
from scipy import stats 
from scipy.stats import linregress
from numpy import where


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


#lagged correlation -- forward looking (extreme first)
extreme_first['next_day_returns'] = extreme_first['daily_returns'].shift(-1)
correlation_lagged = extreme_first['sentiment'].corr(extreme_first['next_day_returns'])
print(correlation_lagged)


clean = extreme_first[['sentiment', 'next_day_returns']].dropna()
corr2, pval2 = stats.pearsonr(clean['sentiment'], clean['next_day_returns'])
print(f"Lagged correlation: {corr2:.4f}, p-value: {pval2:.4f}")

first_presidency = first_presidency.sort_values('date').reset_index(drop=True)

results = []

#linear regression model
for i in range(120, len(first_presidency)):
    window = first_presidency.iloc[i-120:i]
    slope, intercept, rval, pval, std = linregress(window['sentiment'], window['daily_returns'])

    todays_sentiment = first_presidency.iloc[i]['sentiment']
    predicted = slope * todays_sentiment + intercept

    #actual return for the current day
    actual = first_presidency.iloc[i]['daily_returns']
    results.append({'predicted': predicted, 'actual': actual})


results_df = pd.DataFrame(results)
print(results_df.head(10))
    
#add new columns to results_df
results_df['position'] = np.where(results_df['predicted'] > 0, 1, 0)
position_change = results_df['position'].diff().abs().fillna(0)
results_df['strategy_return'] = results_df['position'] * results_df['actual'] - (0.001 * position_change)
position_change = results_df['position'].diff().abs().fillna(0)

results_df['equity_curve'] = (1 + results_df['strategy_return']).cumprod()

print(f"Final equity: {results_df['equity_curve'].iloc[-1]:.4f}")
print(f"Buy and hold: {(1 + results_df['actual']).prod():.4f}")

#sharpe 
mean_r = results_df['strategy_return'].mean()
std_r = results_df['strategy_return'].std()
sharpe = (mean_r - 0.02/252) / std_r * np.sqrt(252)
print(f"Sharpe: {sharpe:.4f}")

#max drawdown 
rolling_max = results_df['equity_curve'].cummax()
drawdown = (results_df['equity_curve'] - rolling_max) / rolling_max
max_dd = drawdown.min()
print(f"Max drawdown: {max_dd:.4f}")

hit_rate = (np.sign(results_df['predicted']) == np.sign(results_df['actual'])).mean()
print(f"Hit rate: {hit_rate:.4f}")