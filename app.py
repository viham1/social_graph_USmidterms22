from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import tweepy
from tqdm import tqdm
import json
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import JSONB
import time

app = Flask(__name__)

database_uri = "postgresql://postgres:password@localhost/social"
app.config["SQLALCHEMY_DATABASE_URI"] = database_uri

db = SQLAlchemy(app)

class Tweet(db.Model):
    __tablename__ = "tweets"
    id = db.Column(db.Integer, primary_key=True)
    tweet = db.Column(JSONB)
    
with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        print(e)
        db.session.rollback()
    db.session.commit()

bearer_token = "AAAAAAAAAAAAAAAAAAAAAGVQjAEAAAAAjkQ%2FGPS0L%2FzlmHDhlntcZi6vf7o%3D5e7M8fR6VcwwyIpFEPabyI8sBFO5kTmBkl9ZfVth7O2ebPNb6C"
consumer_key="s26YwxNnw22tOwxbIw64HiId0"
consumer_secret="n5AaWFibicQfh9FozTr1va9Mr3li0gBqik9TXx60FzqdZvfJxA"
access_token="1485659958284898308-tINI07axvyw1dmIPX0hkuHfUJT3zyO"
access_token_secret="Ln8BKhVgSCzQ1ETlbXfcRwAqD69YHh7SSx7RKVcIDEhyb"


auth = tweepy.OAuth1UserHandler(
   consumer_key, consumer_secret, access_token, access_token_secret
)
api = tweepy.API(auth)

total_tweets = 100000



with app.app_context():
    def limit_handled(cursor):
        while True:
            try:
                yield cursor.next()
            except tweepy.errors.TweepyException:
                print('Reached rate limite. Sleeping for >15 minutes')
                time.sleep(15 * 61)
            except StopIteration:
                break

    tweets = []
    i=0

    search = limit_handled(tweepy.Cursor(api.search_tweets,q="midterms OR electionday",count=200, tweet_mode='extended').items())
    for tweet in search:
        try:
            record = Tweet(tweet=tweet._json)
            db.session.add(record)
            i+= 1
            if i%1000== 0:
                db.session.commit()
        except:
            pass



if __name__ == '__main__':
   app.run()
