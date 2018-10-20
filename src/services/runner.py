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

        # run social channel specific methods
        if self.channel == 'reddit':
            social = Reddit(self.user)
        elif self.channel == 'twitter':
            social = Twitter(self.user)
        elif self.channel == 'instagram':
            social = Instagram(self.user)
        else:
            return

        try:
            # attempt scrape
            social.scrape()
        except Exception as e:
            # report error
            self.slack.post({ 'text': e })

        # if post is new build message
        # and post to slack
        if social.is_new():
            message = social.message()
            self.slack.post(message)
