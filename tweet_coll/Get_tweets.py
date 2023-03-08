import tweepy
import os 
import logging
import pymongo
from dotenv import dotenv_values, find_dotenv
from time import sleep


# GETTING ENVIRONMETAL VARIABLES
ENV = dict(dotenv_values(find_dotenv()))
#API_Key = ENV.get('API_Key')
#API_Key_Secret = ENV.get('API_Key_Secret')
BEARER_TOKEN = os.getenv('BEARER_TOKEN')
MONGO_HOST = os.getenv('MONGO_HOST')#name of the service or name of the container


if not BEARER_TOKEN:
    logging.error('BEARER_TOKEN empty!')

## twitter conuction
#twitter_client = tweepy.Client(BEARER_TOKEN)
client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    wait_on_rate_limit=True,
)
# - means NOT
search_query = "#FIFA -is:retweet -is:reply -is:quote lang:en -has:links"

while True:
    client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    wait_on_rate_limit=True,
    )

    cursor = tweepy.Paginator(
        method=client.search_recent_tweets,
        query=search_query,
        tweet_fields=['id','author_id', 'created_at', 'public_metrics'],
        user_fields=['username']
    ).flatten(limit=50)

        #Mongo DataBase conuction
        #uri = f"mongodb://{MONGO_HOST}:{MONGO_PORT}"
    client = pymongo.MongoClient(host=MONGO_HOST,port=27017)
    db= client.twitter
        # uplod the tweets to DataBase
        
    #for index,tweet in enumerate(cursor):
        #dict_t= {'id':index,'tweet':tweet.text}
        #db.tweet_dic.insert_one(dict_t)
    for tweet in cursor:
        db.tweet_dic.insert_one(dict(tweet))


    client.close()
    sleep (10)
    # IF i want to Drop the Database or the collaction 
    #db_tweet.tweet_dic.drop()