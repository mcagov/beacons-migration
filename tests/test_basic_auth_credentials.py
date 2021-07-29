import os

from src.helpers.api_basic_auth_helper import get_api_basic_auth_credentials


def test_defaults_to_basic_auth_credentials():
    assert get_api_basic_auth_credentials() == ('user', 'password')


def test_basic_auth_credentials_taken_from_env_variables():
    os.environ['API_BASIC_AUTH_USERNAME'] = 'migrate-me'
    os.environ['API_BASIC_AUTH_PASSWORD'] = 'migrate-me-more'

    assert get_api_basic_auth_credentials() == ('migrate-me', 'migrate-me-more')
