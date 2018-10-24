#import from application
from services.slack import Slack
from social.reddit import Reddit
from social.twitter import Twitter
from social.instagram import Instagram

class Runner:

    def __init__(self, channel, user):

        # store user and channel
        self.channel = channel
        self.user = user
        self.slack = Slack()

    def stalk(self):

        # fallback if scrape fails
        post_list = []

        # run social channel specific methods
        if self.channel == 'reddit':
            social = Reddit(self.user)
        elif self.channel == 'twitter':
            social = Twitter(self.user)
        elif self.channel == 'instagram':
            social = Instagram(self.user)
        else:
            return

        # attempt scrape and append to post_list
        try:
            new_posts = social.scrape()
            post_list = post_list + new_posts
        except Exception as e:
            self.slack.post({ 'text': e })

        # Iterate through posts returned from scrape
        # if post is new build message and post to slack
        for post in post_list:
            message = social.message(post)
            self.slack.post(message)
