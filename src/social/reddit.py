# import from system
import time
import json

# iimport from dependencies
import requests
import yaml

# import config
with open('config.yml', 'r') as config:
    config = yaml.load(config)

# module constants
REDDIT_ICON = 'https://www.redditstatic.com/desktop2x/img/favicon/favicon-32x32.png'
SLEEP_TIME = config['app']['sleep_time']
REQ_HEADERS = { 'User-Agent': 'S.T.A.L.K.E.R. by mikeydunn' }

class Reddit:

    def __init__(self, user):

        # initialize class props
        self.user = user
        self.data = {}

    def scrape(self):

        # use unique headers for reddit throttling
        url = f'https://www.reddit.com/user/{self.user}.json'

        # request users json
        response = requests.get(url, headers=REQ_HEADERS)
        json = response.json()
        self.data = json['data']['children'][0]['data']

        # return stored data
        return self.data

    def message(self):

        # storing json objects for building message
        output = { 'attachments': [] }
        latest_post = self.data
        screen_name = latest_post['author']
        author_name = f'u/{screen_name}'
        footer = latest_post['subreddit_name_prefixed']
        ts = latest_post['created_utc']
        permalink = latest_post["permalink"]
        pretext = f'https://reddit.com{permalink}'

        # if post_hint exists, use submission keys
        if 'post_hint' in latest_post:
            title = latest_post['title']
            title_link = latest_post['url']
            text = latest_post['selftext']
            thumb_url = latest_post['thumbnail']

        # else use comment keys
        else:
            title = latest_post['link_title']
            title_link = latest_post['link_url']
            text = latest_post['body']
            thumb_url = ''

        # build message
        message = {
            'pretext': pretext,
            'author_name': author_name,
            'title': title,
            'title_link': title_link,
            'text': text,
            'thumb_url': thumb_url,
            'footer': footer,
            'footer_icon': REDDIT_ICON,
            'ts': ts
        }

        # append message to slack attachments field
        output['attachments'].append(message)

        # return formatted message
        return output

    def is_new(self):

        # if invalid dict return false
        if 'created_utc' not in self.data:
            return False

        # calculate times for check
        latest_post = self.data
        post_time = latest_post['created_utc']
        current_time = time.time()
        last_check_time = current_time - SLEEP_TIME

        # if the post time is larger, its newer than last check
        return True if post_time > last_check_time else False
