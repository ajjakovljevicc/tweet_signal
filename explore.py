import json
import pprint
import re
import pandas as pd
import html

#open data file
with open("data/trumptweets.json", encoding="utf-8") as f:
    tweets = json.load(f)

#append raw data into new list
tweetrows = []

for tweet in tweets:
    tweetrows.append({"timestamp": tweet["date"], "text": tweet["text"], "is_retweet": tweet["isRetweet"], "favorites": tweet["favorites"], "retweets": tweet["retweets"]})

df = pd.DataFrame(tweetrows)

#remove retweets
df["is_retweet"] = df["is_retweet"] == "t"
df = df[~df["is_retweet"]]
df = df.drop(columns=["is_retweet"])

#convert and filter time
df["timestamp"] = pd.to_datetime(df["timestamp"]) #convert from utc to standard datetime
df = df.sort_values("timestamp")
df = df.reset_index(drop=True)

#get the most tweeted days 
#print(df["timestamp"].min())
#print(df["timestamp"].max())
#print(df["timestamp"].dt.date.value_counts().head(10))

#regex method to remove artifacts and urls
def clean_text(txt):
    p = r'https?://\S+|www\.\S+'
    cleanedtext = re.sub(p, "", txt)
    cleanedtext = html.unescape(cleanedtext)
    return cleanedtext

#tweet column filter out urls etc
df["text"] = df["text"].apply(clean_text)

df.to_csv('data/tweets_clean.csv', index=False)
