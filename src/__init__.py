from os.path import dirname, join, realpath

import yaml

with open(join(dirname(realpath(__file__)), 'config.yml'), 'r') as r:
    config = yaml.safe_load(r)
