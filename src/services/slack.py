#import from dependencies
import yaml
import requests

# import config
with open('config.yml', 'r') as config:
    config = yaml.load(config)

class Slack:
    def __init__(self):
        self.webhook_url = config['slack']['webhook_url']

    def post(self, message):
        requests.post(self.webhook_url, json=message)
