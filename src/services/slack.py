#import from dependencies
import yaml
import requests

# import config
with open('config.yml', 'r') as config:
    config = yaml.load(config)

# module constants
WEBHOOK_URL = config['auth']['slack']['webhook_url']

class Slack:
    def post(self, message):
        requests.post(WEBHOOK_URL, json=message)
