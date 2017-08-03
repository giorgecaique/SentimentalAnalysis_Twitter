import sys

class Tweet:
    def __init__(self, reaction=None, date=None, query=None, user=None, text=None):
        self.reaction = reaction
        self.date = date
        self.query = query
        self.user = user
        self.text = text
