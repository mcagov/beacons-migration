import os

user = os.environ.get('API_BASIC_AUTH_USERNAME', 'user')
password = os.environ.get('API_BASIC_AUTH_PASSWORD', 'password')


def get_api_basic_auth():
    return user, password
