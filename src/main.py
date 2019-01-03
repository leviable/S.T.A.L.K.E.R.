# import from system
import time
import sys

# import from dependencies
import yaml

# import from app
from .services.messaging import Messaging
from .services.runner import Runner
from . import config

def main():
    # variable declerations
    social_channels = config['social_channels']
    sleep_time = config['app']['sleep_time']
    messaging = Messaging()
    start_message = 'now stalking...'
    exit_message = 'ending stalk...'

    # output running status
    messaging.post({ 'text': start_message })

    # loop through runners until killed
    while True:
        try:
            # start cycle of runners
            initialize_runners(social_channels)
            # wait for next cycle
            time.sleep(sleep_time)
        except KeyboardInterrupt:
            # output ending status
            messaging.post({ 'text': exit_message })
            # graceful exit
            sys.exit(0)

def initialize_runners(social_channels):

    # start a runner for each user in a channel
    for channel, users in social_channels.items():
        if isinstance(users, list):
            for user in users:
                runner = Runner(channel, user)
                runner.stalk()

if __name__ == "__main__":
    main()
