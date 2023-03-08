import time
from sqlalchemy import create_engine
import os
# from dotenv import dotenv_values, find_dotenv
import logging
import requests
import pandas as pd
import pyjokes
while True:


logging.basicConfig(level='INFO')

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
webhook_url = os.getenv('Webhook_URL_SLACK')

# CONNECT THE CLIENT TO POSTGRESQL
uri = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@postgresdb:5432/{POSTGRES_DB}'
pg = create_engine(uri, echo=True)
pg.connect()
time.sleep(30)

#joke = pyjokes.get_joke()
#data = {'text': joke}
#requests.post(url=webhook_url, json = data)


# EXTRACT TWEETS FROM POSTGRES DB
query = '''SELECT * FROM tweets;'''
result = pg.execute(query)
data_all = result.fetchall()
print('------This is the data from postgresql ------')
print(type(data_all)) # list of tuples [(ind, text, score), (ind, text, score), ...]
print(data_all)
print('---------------------')
# turn list of tuples into dataframe
df = pd.DataFrame(data_all, columns=['ind', 'tweet', 'sentiment'])
# find the most positive tweet and corresponding sentiment
text = df['tweet'].iloc[df['sentiment'].argmax()]
score = df['sentiment'].iloc[df['sentiment'].argmax()]
# edit the content of slack post
post = f'\n \n Hey check this tweet: \n {text} \n According to vader it is the most positive of last tweets about Bernie with a sentiment score of: \n {score} \n \n'
logging.warning('------------- This is the post going to be posted on slack --------------')
logging.warning(post)
logging.warning(type(post))
#logging.warning(type(joke))
logging.warning('--------------------')
# post on slack
requests.post(url=webhook_url, json = {'text': post})