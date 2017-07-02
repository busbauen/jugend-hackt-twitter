#!/usr/bin/env python
import twitter
import random
import sys
import pickle
import os
from config import *

class Client(object):
    def __init__(self):
        """initialize twitter api"""
        self._api = twitter.Api(consumer_key, consumer_secret, access_token_key, access_token_secret)

    def get_tweets_by_user(self, username):
        """get all tweets by username
            para username: String (twitter username)
            returns: List [ objects of twitter.models.Status ]
        """

        #thx to https://gist.github.com/yanofsky/5436496
        alltweets = []  
        try:
            new_tweets = self._api.GetUserTimeline(screen_name = username,count=200)
        except twitter.error.TwitterError as e:
            print("username does not exist.")
            sys.exit(1)
            
        alltweets.extend(new_tweets)

        oldest = alltweets[-1].id - 1

        while len(new_tweets) > 0:
            new_tweets = self._api.GetUserTimeline(screen_name = username,count=200,max_id=oldest)
            alltweets.extend(new_tweets)
            oldest = alltweets[-1].id - 1
        
        return alltweets

    def dump_tweets(self, username):
        """serialize all tweets of a user to "raw/`username`.pickle"
            para:  username: String (twitter username)
        """

        list_tweets = self.get_tweets_by_user(username)
        pickle.dump(list_tweets, open("raw/" + username + ".pickle", "wb"))


    def optimize(self):
        """load all tweets and save only the top 35 to opti/"""
        for f in os.listdir("raw"):
            list_tweets = pickle.load(open("raw/" + f, "rb"))
            best_tweets = [t for t in sorted(list_tweets, key=lambda t: t.favorite_count, reverse=True)[:25]]
            pickle.dump(best_tweets, open("opti/" + f, "wb"))

def generate_question():
    """generate a question. choose a random file to load. then a random tweet"""
    choices = os.listdir("opti")
    solution_user = random.choice(choices)
    list_questions = pickle.load(open("opti/" + solution_user, "rb"))
    question = random.choice(list_questions)
    return (question.text, choices, solution_user.split('.')[0])

if __name__ == '__main__':
    api = Client()
    api.get_tweets_by_user("barackobama")
    #api.dump_tweets("barackobama")
    #api.optimize()
    #print(api.generate_question())
