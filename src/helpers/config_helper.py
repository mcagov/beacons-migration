import configparser

parser = configparser.ConfigParser()
parser.read('./config/config.ini')


def get_config_parser():
    return parser
