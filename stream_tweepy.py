""" 
    Muhammad Jaury
    muhjaury@gmail.com
"""

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from elasticsearch import Elasticsearch

import json 
import pymongo
import tw_credentials
import sentiment

# elasticserver = 'http://127.0.0.1'
# elasticport = 9200
# elasticurl = elasticserver+':'+str(elasticport)+'/'
# elasticusername = ''
# elasticpassword = ''
# es = Elasticsearch([elasticserver], port=elasticport, http_auth=(elasticusername,elasticpassword))

def full_text_check(data):
    if("retweeted_status" in data) and ("extended_tweet" in data):
        # tweet retweet
        status = True
    else:
        # original tweet
        status = False
    return status

# # # # TWITTER STREAMER # # # #
class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """
    def __init__(self):
        pass

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # This handles Twitter authetification and the connection to Twitter Streaming API
        listener = StdOutListener(fetched_tweets_filename)
        auth = OAuthHandler(tw_credentials.CONSUMER_KEY, tw_credentials.CONSUMER_SECRET)
        auth.set_access_token(tw_credentials.ACCESS_TOKEN, tw_credentials.ACCESS_TOKEN_SECRET)
        stream = Stream(auth, listener)

        # This line filter Twitter Streams to capture data by the keywords: 
        stream.filter(track=hash_tag_list)


# # # # TWITTER STREAM LISTENER # # # #
class StdOutListener(StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout.
    """
    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename
        self.counter = 0
        self.limit = 5

    def on_data(self, data):
        try:
            
            #Connect to MongoDB
            client = pymongo.MongoClient()
            db = client.final

            datajson = json.loads(data)
            created_at = datajson['created_at']
            
            t_check = full_text_check(data)
            tweet = ''
            if t_check:
                if datajson['is_quote_status'] == True:
                    tweet = str(datajson['retweeted_status']['text'])
                else:
                    tweet = str(datajson['retweeted_status']['extended_tweet']['full_text'])
            else:
                tweet = str(datajson['text'])
            
            
            datajson['norm_text'], datajson['sentiment'] = sentiment.sentiprocess(tweet)

            print("Tweet collected at " + str(created_at))
            print("Tweet is '" +str(datajson['norm_text'])+"'")
            print("Sentiment is "+str(datajson['sentiment']))
            print("")
            
            #Insert to MongoDB
            db.twitter_stream.insert(datajson)
            #Insert to Elasticsearch
            #res = es.index(index='social_twitter',doc_type='tweets',body=datajson)

            #with open(self.fetched_tweets_filename, 'a') as tf:
                #tf.write(data)
                
            #with open(self.fetched_tweets_filename, 'w') as json_file:
                #json.dump(datajson,json_file)

            self.counter += 1
            if self.counter < self.limit:
                return True
            else:
                return False
        except BaseException as e:
            print("Error on_data %s" % str(e))

    def on_error(self, status):
        print(status)

 
if __name__ == '__main__':
 
    # Authenticate using config.py and connect to Twitter Streaming API.
    hash_tag_list = ["kabar", "Kabar", "pagi", "siang", "malam", "Pagi", "Siang", "Malam"]
    fetched_tweets_filename = "test.json"

    twitter_streamer = TwitterStreamer()
    twitter_streamer.stream_tweets(fetched_tweets_filename, hash_tag_list)