
# coding: utf-8

# # Análise de sentimento no Twitter - Abordagem 2

# Exemplo de usabilidade: Analisar reação do público aos acontecimentos.
#
# Exemplos de áreas que dependem dessa informação:
#     - Marketing
#     - Governo
#     - Psicologia
#
# Fonte dos dados: http://help.sentiment140.com/for-students/

# **Importando os módulos**

# Desenvolvido por Giorge Caique

# In[1]:

import sys, csv, tweepy
from textblob import TextBlob
from Library import *
import requests
import pandas as pd


# **Realizando autenticação na API do Twitter**

# In[2]:

CONSUMER_KEY = 'yXKMKyVm0YmkzMw6e9zAKg2U3'
CONSUMER_SECRET = 'kjmviFnWNPocmBy0xtFxndQ17oKluLM5Ghgu7IQoVUix4HHs3K'
ACCESS_TOKEN = 	'1567104799-zC1CJwjfYWiPAOI9325WLZWe3Z5xyIVdvX4338m'
ACCESS_SECRET = '2U9iV3xy5kFVojA7pwFxkPxasSCZ2qs9hT6asavdSPzdg'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth)


# **Populando o dataset de teste**

# In[3]:

def populate(dataset_file):
    tweets =[]
    with open(dataset_file, newline=None) as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            item = row[0].split(';')

            reaction = None
            if int(item[0]) == 0:
                reaction = "negative"
            elif int(item[0]) == 2:
                reaction = "neutral"
            elif int(item[0]) == 4:
                reaction = "positive"

            tweet = Tweet(reaction,item[2],item[3],item[4], item[5])
            tweets.append((reaction, tweet.query, tweet.text))
            df = pd.DataFrame(tweets, columns=['reaction', 'query', 'text'])
        return df


# **Testando modelo**

# In[4]:

df = populate('dataset.csv')
reaction = 'neutral'
total = 0
accuracy = 0
for text, react in zip(df['text'], df['reaction']):
    total += 1
    analysis = TextBlob(text)
    if(analysis.polarity > 0):
        reaction = 'positive'
    elif(analysis.polarity < 0):
        reaction = 'negative'
    else:
        reaction = 'neutral'
    print('Text:',text.encode())
    print("Predicted reaction: %s -" % reaction, 'Real reaction:', react)
    print('Polarity:', round(analysis.polarity * 100, 2),'%', 'Subjectivity:', round(analysis.subjectivity * 100, 2),'%\n')
    if(str(reaction) == str(react)):
        accuracy += 1

print('Accuracy: ', round(accuracy / total * 100, 2), '%\n')


# # Analisando novos tweets

# In[5]:

public_tweets = tweepy.Cursor(api.search,q="Dunkirk", rpp=100, count=20, result_type="recent", include_entities=False, encode="utf-8",lang='en').items(30)
for tweet in public_tweets:
    analysis = TextBlob(tweet.text)
    if(analysis.polarity > 0):
        reaction = 'positive'
    elif(analysis.polarity < 0):
        reaction = 'negative'
    else:
        reaction = 'neutral'
    print('Text:',analysis)
    print("Predicted reaction: %s" % reaction)
    print('Polarity:', round(analysis.polarity * 100, 2),'%', 'Subjectivity:', round(analysis.subjectivity * 100, 2),'%\n')
