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

    def scrape(self):

        # build request url
        url = f'https://www.reddit.com/user/{self.user}.json'

        # request users posts
        # use unique headers for reddit throttling
        response = requests.get(url, headers=REQ_HEADERS)
        json = response.json()

        # filter list of new posts
        posts = json['data']['children']
        new_posts = list(filter(self._is_new, posts))

        # return list of new raw posts
        return new_posts

    def message(self, post):

        # storing json objects for building message
        post_data = post['data']
        screen_name = post_data['author']
        author_name = f'u/{screen_name}'
        footer = post_data['subreddit_name_prefixed']
        ts = post_data['created_utc']
        permalink = post_data["permalink"]
        pretext = f'https://reddit.com{permalink}'

        # if post_data_hint exists, use submission keys
        if 'post_data_hint' in post_data:
            title = post_data['title']
            title_link = post_data['url']
            text = post_data['selftext']
            thumb_url = post_data['thumbnail']

        # else use comment keys
        else:
            title = post_data['link_title']
            title_link = post_data['link_url']
            text = post_data['body']
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

        # return formatted messag
        return message

    def _is_new(self, post):

        # if invalid dict return false
        if 'created_utc' not in post['data']:
            return False

        # calculate times for check
        post_time = post['data']['created_utc']
        current_time = time.time()
        last_check_time = current_time - SLEEP_TIME

        # if the post time is larger, its newer than last check
        return True if post_time > last_check_time else False
