import pandas as pd 
import numpy as np
from scipy import stats 
from scipy.stats import linregress
from numpy import where

events = {
    'Soleimani assassination':  '2020-01-03',
    'Iran missile retaliation': '2020-01-08',
    'Iran deal withdrawal':     '2018-05-08',
    'Steel tariff announcement':'2018-03-01',
    'China tariffs escalation': '2019-05-05',
    'Phase One trade deal':     '2020-01-15',
    'Jan 6 Capitol riot':       '2021-01-06',
}

tweet_sentiment = pd.read_csv('data/tweets_sentiment.csv')
