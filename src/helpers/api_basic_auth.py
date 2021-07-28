import os


def get_api_basic_auth():
    user = os.environ.get('API_BASIC_AUTH_USERNAME', 'user')
    password = os.environ.get('API_BASIC_AUTH_PASSWORD', 'password')

    return user, password
