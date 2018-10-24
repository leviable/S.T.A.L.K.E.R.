# import from system
import time
import json

# import from dependencies
from application_only_auth import Client
import requests
import yaml

# import config
with open('config.yml', 'r') as config:
    config = yaml.load(config)

# module constants
API_KEY = config['auth']['twitter']['api_key']
SECRET_KEY = config['auth']['twitter']['secret_key']
SLEEP_TIME = config['app']['sleep_time']
TWITTER_API_URL = 'https://api.twitter.com/1.1/'
TWITTER_API_TIMELINE_PATH = 'statuses/user_timeline.json'
TWITTER_NAME = 'Twitter'
TWITTER_ICON = 'https://abs.twimg.com/favicons/favicon.ico'
TWITTER_TS_PATTERN = '%a %b %d %H:%M:%S %z %Y'
TWITTER_MESSAGE_REQUEST_COUNT = 10

class Twitter:

    def __init__(self, user):

        # build client and class props
        self.client = Client(API_KEY, SECRET_KEY)
        self.user = user

    def scrape(self):

        # build request url
        params = f'screen_name={self.user}&count={TWITTER_MESSAGE_REQUEST_COUNT}&tweet_mode=extended'
        url = f'{TWITTER_API_URL}{TWITTER_API_TIMELINE_PATH}?{params}'

        # request users posts
        posts = self.client.request(url)

        # filter list of new posts
        new_posts = list(filter(self._is_new, posts))

        # return stored data
        return new_posts

    def message(self, post):

        # storing json objects for building message
        tweet_id = post['id']
        author_name = post['user']['screen_name']
        text = post['full_text']

        # convert twitter time to epoch
        ts_twitter = post['created_at']
        ts = int(time.mktime(time.strptime(ts_twitter, TWITTER_TS_PATTERN)))

        # pretext base stored for retweet
        pretext_base = f'https://twitter.com/{author_name}/status/'
        pretext = f'{pretext_base}{tweet_id}'

        # overwrite with retweet info
        is_retweet = True if 'retweeted_status' in self.data else False

        if is_retweet:
            # retweet specific overwrites
            retweet_author = post['retweeted_status']['user']['screen_name']
            author_name = f'@{author_name} - retweeted @{retweet_author}'
            text = post['retweeted_status']['full_text']
            tweet_id = post['retweeted_status']['id']
            pretext = f'{pretext_base}{tweet_id}'

        # build message
        message = {
            'pretext': pretext,
            'author_name': author_name,
            'text': text,
            'footer': TWITTER_NAME,
            'footer_icon': TWITTER_ICON,
            'ts': ts
        }

        # return formatted message
        return message

    def _is_new(self, post):

        # if invalid dict return false
        if 'created_at' not in post:
            return False

        # calculate times for check
        twitter_ts = post['created_at']
        post_time = int(time.mktime(time.strptime(twitter_ts, TWITTER_TS_PATTERN)))
        current_time = time.time()
        last_check_time = current_time - SLEEP_TIME

        # if the post time is larger, its newer than last check
        return True if post_time > last_check_time else False
