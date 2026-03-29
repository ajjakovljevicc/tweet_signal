import yfinance as yf
import pprint

spydata = yf.download("SPY", start="2009-05-04", end="2021-01-08")

spydata["daily_return"] = spydata["Close"].pct_change()

print(spydata[["Close", "daily_return"]].head(10))

spydata.to_csv('data/spy_clean.csv')