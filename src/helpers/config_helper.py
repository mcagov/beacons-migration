import configparser
import os

parser = configparser.ConfigParser()
parser.read('./config/config.ini')
environment = os.environ.get('ENVIRONMENT', 'LOCAL')


def get_config_parser():
    return parser[environment]
