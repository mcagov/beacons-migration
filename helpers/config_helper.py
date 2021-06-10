import configparser
import requests
import datetime
import time

parser = configparser.ConfigParser()
parser.read('./config/config.ini')


def get_config_parser():
    return parser
