#import from dependencies
import yaml
import requests

# import config
with open('config.yml', 'r') as config:
    config = yaml.load(config)

# module constants
SLACK_WEBHOOK_URL = config['auth']['slack']['webhook_url']

class Messaging:
    def post(self, message):

        try:
            # attempt to post to slack
            output = { 'attachments': [message] }
            requests.post(SLACK_WEBHOOK_URL, json=output)
        except:
            # on error print message to console
            print(message)
