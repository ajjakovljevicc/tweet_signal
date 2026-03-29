import pandas as pd
import json 

df1 = pd.read_csv('data/tweets_clean.csv')
df2 = pd.read_csv('data/spy_clean.csv')

print(df1.head(10))
print(df2.head(10))