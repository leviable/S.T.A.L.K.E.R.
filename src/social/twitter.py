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

class Twitter:

    def __init__(self, user):

        # build client and class props
        self.client = Client(API_KEY, SECRET_KEY)
        self.user = user
        self.data = {}

    def scrape(self):

        # build request url
        params = f'screen_name={self.user}&count=1&tweet_mode=extended'
        url = f'{TWITTER_API_URL}{TWITTER_API_TIMELINE_PATH}?{params}'

        # request users json
        response = self.client.request(url)
        self.data = response[0]

        # return stored data
        return self.data

    def message(self):

        # storing json objects for building message
        output = { 'attachments': [] }
        latest_post = self.data
        tweet_id = latest_post['id']
        author_name = latest_post['user']['screen_name']
        text = latest_post['full_text']

        # convert twitter time to epoch
        ts_twitter = latest_post['created_at']
        ts = int(time.mktime(time.strptime(ts_twitter, TWITTER_TS_PATTERN)))

        # pretext base stored for retweet
        pretext_base = 'https://twitter.com/{screen_name}/status/'
        pretext = f'{pretext_base}{tweet_id}'

        # overwrite with retweet info
        is_retweet = True if 'retweeted_status' in self.data else False

        if is_retweet:
            # retweet specific overwrites
            retweet_author = latest_post['retweeted_status']['user']['screen_name']
            author_name = f'@{author_name} - retweeted @{retweet_author}'
            text = latest_post['retweeted_status']['full_text']
            tweet_id = latest_post['retweeted_status']['id']
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

        # append message to slack attachments field
        output['attachments'].append(message)

        # return formatted message
        return output

    def is_new(self):

        # if invalid dict return false
        if 'created_at' not in self.data:
            return False

        # calculate times for check
        latest_post = self.data
        ts_twitter = latest_post['created_at']
        post_time = int(time.mktime(time.strptime(ts_twitter, TWITTER_TS_PATTERN)))
        current_time = time.time()
        last_check_time = current_time - SLEEP_TIME

        # if the post time is larger, its newer than last check
        return True if post_time > last_check_time else False
