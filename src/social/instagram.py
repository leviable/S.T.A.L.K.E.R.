# import from system
import time
import json

# iimport from dependencies
import requests
import yaml

# import config
with open('config.yml', 'r') as config:
    config = yaml.load(config)

class Instagram:

    def __init__(self, user):

        # initialize class props
        self.user = user
        self.data = {}

    def scrape(self):

        # authentication variables
        auth_url = 'https://www.instagram.com/accounts/login/'
        auth_url_main = auth_url + 'ajax/'
        username = config['auth']['instagram']['username']
        password = config['auth']['instagram']['password']
        auth = {'username': username, 'password': password}
        headers = {'referer': "https://www.instagram.com/accounts/login/"}

        # use a session to store auth cookies
        with requests.Session() as session:

            # retrieve and set auth cookies
            req = session.get(auth_url)
            headers['x-csrftoken'] = req.cookies['csrftoken']
            session.post(auth_url_main, data=auth, headers=headers)

            # get and store user json
            user_url = f'https://www.instagram.com/{self.user}?__a=1'
            response = session.get(user_url)
            json = response.json()
            self.data = json['graphql']['user']

        # return stored data
        return self.data

    def message(self):

        # storing json objects for building message
        output = { 'attachments': [] }
        latest_post = self.data['edge_owner_to_timeline_media']['edges'][0]['node']
        author_name = latest_post['owner']['username']
        text = latest_post['edge_media_to_caption']['edges'][0]['node']['text']
        image_url = latest_post['display_url']
        thumb_url = latest_post['thumbnail_src']
        footer = 'Instagram'
        footer_icon = 'https://www.instagram.com/static/images/ico/apple-touch-icon-76x76-precomposed.png/4272e394f5ad.png'
        ts = latest_post['taken_at_timestamp']
        shortcode = latest_post["shortcode"]
        pretext = f'https://www.instagram.com/p/{shortcode}'

        # build message
        message = {
            'pretext': pretext,
            'author_name': author_name,
            'text': text,
            'image_url': image_url,
            'thumb_url': thumb_url,
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
        if 'edge_owner_to_timeline_media' not in self.data:
            return False

        # calculate times for check
        latest_post = self.data['edge_owner_to_timeline_media']['edges'][0]['node']
        post_time = latest_post['taken_at_timestamp']
        current_time = time.time()
        sleep_time = config['app']['sleep_time']
        last_check_time = current_time - sleep_time

        # if the post time is larger, its newer than last check
        return True if post_time > last_check_time else False
