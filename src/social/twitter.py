# import from system
import time
import json

# import from dependencies
from application_only_auth import Client
import requests
import yaml

# import config
from .. import config

# module constants
SLEEP_TIME = config['app']['sleep_time']
TWITTER_API_URL = 'https://api.twitter.com/1.1/'
TWITTER_API_TIMELINE_PATH = 'statuses/user_timeline.json'
TWITTER_TS_PATTERN = '%a %b %d %H:%M:%S %z %Y'
TWITTER_MESSAGE_REQUEST_COUNT = 10

class Twitter:

    def __init__(self, user):

        api_key = config['auth']['twitter']['api_key']
        secret_key = config['auth']['twitter']['secret_key']

        # build client and class props
        self.client = Client(api_key, secret_key)
        self.user = user

    def scrape(self):

        # build request url
        params = f'screen_name={self.user}&count={TWITTER_MESSAGE_REQUEST_COUNT}&tweet_mode=extended'
        url = f'{TWITTER_API_URL}{TWITTER_API_TIMELINE_PATH}?{params}'

        # request users posts
        posts = self.client.request(url)

        # filter list of new posts
        # reverse posts for correct chronological posting order
        new_posts = list(filter(self._is_new, posts))
        new_posts_reversed = list(reversed(new_posts))

        # return list of new raw posts
        return new_posts_reversed

    def message(self, post):

        # storing json objects for building message
        tweet_id = post['id']
        screen_name = post['user']['screen_name']
        author_link = f'https://twitter.com/{screen_name}'
        text = f'{author_link}/status/{tweet_id}'

        # build message
        message = {
            'text': text,
            'unfurl_links': True,
            'unfurl_media': True
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
