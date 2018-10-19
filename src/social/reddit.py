#import from dependencies
import time
import requests
import json
import yaml

# import config
with open('config.yml', 'r') as config:
    config = yaml.load(config)

class Reddit:
    def __init__(self, user):
        self.user = user
        self.data = {}

    def scrape(self):
        # use unique headers for reddit throttling
        headers = { 'User-Agent': 'S.T.A.L.K.E.R. by mikeydunn' }
        url = f'https://www.reddit.com/user/{self.user}.json'

        # request users json
        response = requests.get(url, headers=headers)
        self.data = response.json()

        return self.data

    def message(self):
        # storing json objects for building message
        output = { 'attachments': [] }
        latest_post = self.data['data']['children'][0]['data']
        author_name = latest_post['author']
        title = latest_post['link_title']
        title_link = 'https://reddit.com' + latest_post['permalink']
        text = latest_post['body']
        footer = latest_post['subreddit_name_prefixed']
        ts = latest_post['created_utc']

        # build message
        message = {
            "author_name": author_name,
            "title": title,
            "title_link": title_link,
            "text": text,
            "footer": footer,
            "ts": ts
        }

        # attach to output
        output['attachments'].append(message)

        # return slack specific formatted message
        return output

    def is_new(self):
        # if invalid dict return false
        if 'data' not in self.data:
            return False

        # calculate times for check
        latest_post = self.data['data']['children'][0]['data']
        post_time = latest_post['created_utc']
        current_time = time.time()
        sleep_time = config['app']['sleep_time']
        last_check_time = current_time - sleep_time

        # if the post time is larger, its newer than last check
        return True if post_time > last_check_time else False
