import os

from src.helpers.api_basic_auth import get_api_basic_auth


def test_defaults_to_basic_auth_credentials():
    assert get_api_basic_auth() == ('user', 'password')


def test_basic_auth_credentials_taken_from_env_variables():
    os.environ['API_BASIC_AUTH_USERNAME'] = 'migrate-me'
    os.environ['API_BASIC_AUTH_PASSWORD'] = 'migrate-me-more'

    assert get_api_basic_auth() == ('migrate-me', 'migrate-me-more')
