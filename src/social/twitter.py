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

class Twitter:

    def __init__(self, user):

        # gather keys for client
        api_key = config['twitter']['api_key']
        secret_key = config['twitter']['secret_key']

        # build client and class props
        self.client = Client(api_key, secret_key)
        self.user = user
        self.data = {}

    def scrape(self):

        # build request url
        params = f'screen_name={self.user}&count=1&tweet_mode=extended'
        url = f'https://api.twitter.com/1.1/statuses/user_timeline.json?{params}'

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
        screen_name = latest_post['user']['screen_name']
        author_name = f'@{screen_name}'
        text = latest_post['full_text']
        footer = 'Twitter'
        footer_icon = 'https://abs.twimg.com/favicons/favicon.ico'

        # convert twitter time to epoch
        ts_twitter = latest_post['created_at']
        ts_pattern = '%a %b %d %H:%M:%S %z %Y'
        ts = int(time.mktime(time.strptime(ts_twitter, ts_pattern)))

        # pretext base stored for retweet
        pretext_base = 'https://twitter.com/TeamYouTube/status/'
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
            'footer': footer,
            'footer_icon': footer_icon,
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
        ts_pattern = '%a %b %d %H:%M:%S %z %Y'
        post_time = int(time.mktime(time.strptime(ts_twitter, ts_pattern)))
        current_time = time.time()
        sleep_time = config['app']['sleep_time']
        last_check_time = current_time - sleep_time

        # if the post time is larger, its newer than last check
        return True if post_time > last_check_time else False
