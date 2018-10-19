# import from system
import time

# import from dependencies
import yaml

# import from app
from services.runner import Runner

# import config
with open('config.yml', 'r') as config:
    config = yaml.load(config)
    social_channels = config['social_channels']
    sleep_time = config['app']['sleep_time']

# application entry point
def main():

    # start a runner for each user in a channel
    for channel, users in social_channels.items():
        if not isinstance(users, list):
            break

        for user in users:
            runner = Runner(channel, user)
            runner.stalk()

while True:
    main()
    time.sleep(sleep_time)
