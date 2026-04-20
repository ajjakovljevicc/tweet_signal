import pandas as pd
import json 
from datetime import timedelta

tweets = pd.read_csv('data/tweets_clean.csv')
spy = pd.read_csv('data/spy_clean.csv', skiprows=3, header=None, names=["date", "close", "high", "low", "open", "volume", "daily_returns"])

tweets["timestamp"] = pd.to_datetime(tweets["timestamp"])
tweets["date"] = tweets["timestamp"].dt.date

spy["date"] = pd.to_datetime(spy["date"])
spy["date"] = spy["date"].dt.date


def next_trading_day(date):
    if date.weekday() == 5:
        return date + timedelta(days=2)
    elif date.weekday() == 6:
        return date + timedelta(days=1)
    else:
        return date
    
tweets["date"] = tweets["date"].apply(next_trading_day)


mergeddf = pd.merge(tweets, spy, how="inner", on="date")
print(mergeddf.head(10))
mergeddf.to_csv('data/merged.csv', index=False)

merged_cleaned = mergeddf.dropna(subset="text")
merged_cleaned.to_csv('data/merged_cleaned.csv', index=False)