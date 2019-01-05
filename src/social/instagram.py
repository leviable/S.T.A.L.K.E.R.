# import from system
import time
import json

# iimport from dependencies
import requests
import yaml

# import config
from .. import config

# module constants
AUTH_URL = 'https://www.instagram.com/accounts/login/'
AUTH_URL_MAIN = AUTH_URL + 'ajax/'
SLEEP_TIME = config['app']['sleep_time']

class Instagram:

    def __init__(self, user):

        # initialize class props
        self.user = user

    def scrape(self):

        # use a session to store auth cookies
        with requests.Session() as session:

            # login information
            login_username = config['auth']['instagram']['username']
            login_password = config['auth']['instagram']['password']
            login_dict = {'username': login_username, 'password': login_password}

            # retrieve and set auth cookies
            req = session.get(AUTH_URL)
            headers = {'referer': "https://www.instagram.com/accounts/login/"}
            headers['x-csrftoken'] = req.cookies['csrftoken']
            session.post(AUTH_URL_MAIN, data=login_dict, headers=headers)

            # build request url
            user_url = f'https://www.instagram.com/{self.user}?__a=1'

            # request user posts
            response = session.get(user_url)
            data = response.json()

        # filter list of new posts
        posts = data['graphql']['user']['edge_owner_to_timeline_media']['edges']
        new_posts = list(filter(self._is_new, posts))

        # return list of new raw posts
        return new_posts


    def message(self, post):

        # storing json objects for building message
        latest_post = post['node']
        shortcode = latest_post["shortcode"]
        text = f'https://www.instagram.com/p/{shortcode}'

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
        if 'taken_at_timestamp' not in post['node']:
            return False

        # calculate times for check
        post_time = post['node']['taken_at_timestamp']
        current_time = time.time()
        last_check_time = current_time - SLEEP_TIME

        # if the post time is larger, its newer than last check
        return True if post_time > last_check_time else False
