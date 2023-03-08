
import logging 
import sys
import os
import pandas as pd
import pymongo
from sqlalchemy import create_engine
from time import sleep
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

MONGO_USER = os.getenv('MONGO_INITDB_ROOT_USERNAME')
MONGO_PASSWORD = os.getenv('MONGO_INITDB_ROOT_PASSWORD')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')

#from dotenv import dotenv_values, find_dotenv
#while True:
    
    #MongoDB connection and read
MONGO_HOST = os.getenv('MONGO_HOST')
client = pymongo.MongoClient(host=MONGO_HOST, port=27017)
db = client.twitter
sleep(10)
docs = list(db.tweet_dic.find())
client.close()

    #transform the tweets data 
transformed_tweets = []
for tweet in docs:
    analyzer = SentimentIntensityAnalyzer()
    score = analyzer.polarity_scores(tweet['text'])
    tweet['sentiment'] = score.get('compound')  
    tweet['neg'] = score.get('neg')
    tweet['neu'] = score.get('neu')
    tweet['pos'] = score.get('pos')
    transformed_tweets.append(tweet)
    
    #Postgres Create a "connection string"
uri = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@postgresdb:5432/{POSTGRES_DB}'
pg = create_engine(uri, echo=True)
pg.connect()


     # Create, insert and read in Postgres
    #DROP TABLE if exists tweets;
create = '''
CREATE TABLE IF NOT EXISTS tweets (
id BIGINT PRIMARY KEY,
created_at TIMESTAMP,
text VARCHAR(500),
sentiment NUMERIC,
neg FLOAT,
neu FLOAT,
pos FLOAT
);
'''

pg.execute(create)
    
    # Create, insert and read in Postgres
for tweet in transformed_tweets:
    id = tweet.get('text')
    df_keys=['id','created_at','text','sentiment','neg','neu','pos']
    df = pd.json_normalize(tweet, sep='_')
    df[df_keys].to_sql(name="tweets",con=pg, if_exists='append', index=False)
        
pg.close()
    #break
    #sleep(10)

