from Library import *
from collections import Counter

CONSUMER_KEY = 'yXKMKyVm0YmkzMw6e9zAKg2U3'
CONSUMER_SECRET = 'kjmviFnWNPocmBy0xtFxndQ17oKluLM5Ghgu7IQoVUix4HHs3K'
ACCESS_TOKEN = 	'1567104799-zC1CJwjfYWiPAOI9325WLZWe3Z5xyIVdvX4338m'
ACCESS_SECRET = '2U9iV3xy5kFVojA7pwFxkPxasSCZ2qs9hT6asavdSPzdg'

stream = MyStreamer(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET)

stream.statuses.filter(track='Dunkirk')

top_hashtags = Counter(hashtag['text'].lower()
                        for tweet in tweets
                        for hashtag in tweet["entities"]["hashtags"])

print(top_hashtags.most_common(5))
