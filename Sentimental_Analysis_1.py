
# coding: utf-8

# # Análise de sentimento no Twitter - Abordagem 1

# Exemplo de usabilidade: Analisar reação do público aos acontecimentos
# Exemplos de áreas que dependem dessa informação:
#     - Marketing
#     - Governo
#     - Psicologia
#
# Fonte dos dados: http://help.sentiment140.com/for-students/

# **Importando os módulos**

# Desenvolvido por Giorge Caique

# In[1]:

from collections import Counter
from Library import *
import numpy as np
import pandas as pd
from textblob import TextBlob
import sklearn
from sklearn.externals import joblib
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer
import tweepy
import csv


# **Realizando autenticação na API do Twitter**

# In[2]:

CONSUMER_KEY = 'yXKMKyVm0YmkzMw6e9zAKg2U3'
CONSUMER_SECRET = 'kjmviFnWNPocmBy0xtFxndQ17oKluLM5Ghgu7IQoVUix4HHs3K'
ACCESS_TOKEN = 	'1567104799-zC1CJwjfYWiPAOI9325WLZWe3Z5xyIVdvX4338m'
ACCESS_SECRET = '2U9iV3xy5kFVojA7pwFxkPxasSCZ2qs9hT6asavdSPzdg'

# Autenticando para acessar a API do Twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth)


# **Populando o dataset de treinamento**

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


# **Treinando o modelo**

# In[4]:

def train(df, fit_file):
    print('training...\n')
    train_size = 0.8
    vectorizer = CountVectorizer(
        analyzer="word",
        tokenizer=None,
        preprocessor=None,
        stop_words=None
    )
    logreg = LogisticRegression()
    pipe = Pipeline([('vect', vectorizer), ('logreg', logreg)])
    X_train, X_test, Y_train, Y_test = sklearn.model_selection.train_test_split(df.text, df.reaction, train_size=train_size)
    pipe.fit(X_train, Y_train)
    accuracy = pipe.score(X_test, Y_test)
    print("\nAccuracy with {:.0%} of training data: {:.1%}\n".format(train_size, accuracy))
    pipe.fit(df.text, df.reaction)
    joblib.dump(pipe, fit_file)


# **Testando a análise com novas entradas**

# In[5]:

def predict_test(df, fit_file):
    pipe = joblib.load(fit_file)
    texts = df
    accuracy = 0
    total = 0
    for text, react in zip(df['text'], df['reaction']):
        total += 1
        resp = pipe.predict([text])
        print('Text:',text)
        print("Predicted reaction: %s -" % resp[0], 'Real reaction:', react,'\n')
        if(str(resp[0]) == str(react)):
            accuracy += 1

    print('Accuracy: ', round(accuracy / total * 100, 2), '%')


# **Algoritmo**

# In[6]:

df = populate('dataset.csv')
df = df.dropna()
train(df, 'pipefile.txt')
df_test = populate('test.csv')
predict_test(df_test, 'pipefile.txt')


# # Analisando novos tweets

# In[7]:

public_tweets = tweepy.Cursor(api.search,q="Dunkirk", rpp=100, count=20, result_type="recent", include_entities=False, encode="utf-8",lang='en').items(30)
pipe = joblib.load('pipefile.txt')
for tweet in public_tweets:
    resp = pipe.predict([tweet.text])
    print('Tweet:',tweet.text.encode())
    print(" - Predicted reaction: %s" % resp[0],'\n')
