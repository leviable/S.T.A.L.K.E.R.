#import from application
from services.slack import Slack
from social.reddit import Reddit

class Runner:
    def __init__(self, channel, user):
        self.channel = channel
        self.user = user
        self.slack = Slack()

    def stalk(self):
        # run social channel specific methods
        if self.channel == 'reddit':
            social = Reddit(self.user)
        else:
            return

        # attempt scrape
        try:
            social.scrape()
        except:
            print('error scraping')

        # if post is new build message and post to slack
        if social.is_new():
            message = social.message()
            self.slack.post(message)
