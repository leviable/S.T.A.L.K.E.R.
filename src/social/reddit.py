# import from system
import time
import json

# iimport from dependencies
import requests
import yaml

# import config
with open('config.yml', 'r') as config:
    config = yaml.load(config)

class Reddit:

    def __init__(self, user):

        # initialize class props
        self.user = user
        self.data = {}

    def scrape(self):

        # use unique headers for reddit throttling
        headers = { 'User-Agent': 'S.T.A.L.K.E.R. by mikeydunn' }
        url = f'https://www.reddit.com/user/{self.user}.json'

        # request users json
        response = requests.get(url, headers=headers)
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
        title = latest_post['link_title']
        title_link = latest_post['link_url']
        text = latest_post['body']
        footer = latest_post['subreddit_name_prefixed']
        footer_icon = 'https://www.redditstatic.com/desktop2x/img/favicon/favicon-32x32.png'
        ts = latest_post['created_utc']
        pretext = f'https://reddit.com{latest_post["permalink"]}'

        # build message
        message = {
            'pretext': pretext,
            'author_name': author_name,
            'title': title,
            'title_link': title_link,
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
        if 'created_utc' not in self.data:
            return False

        # calculate times for check
        latest_post = self.data
        post_time = latest_post['created_utc']
        current_time = time.time()
        sleep_time = config['app']['sleep_time']
        last_check_time = current_time - sleep_time

        # if the post time is larger, its newer than last check
        return True if post_time > last_check_time else False
