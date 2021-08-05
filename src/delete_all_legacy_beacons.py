import requests

from src.helpers.config_helper import get_config_parser
from src.helpers.api_basic_auth_helper import get_api_basic_auth_credentials


def delete_all():
    api_url = get_config_parser().get('api_url') + '/migrate/delete-all-legacy-beacons'
    response = requests.get(api_url, auth=get_api_basic_auth_credentials())

    if response.status_code != 200:
        message = f'Failed to delete legacy beacon records.  Response {response.json()}'
        raise RuntimeError(message)

    print(f'Successfully deleted all legacy beacons')
