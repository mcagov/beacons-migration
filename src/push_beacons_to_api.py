from datetime import datetime
import requests

import src.get_beacons as get_beacons
from src.beacon_mapper import get_request_body
from src.write_results_to_csv import write_to_csv

from src.helpers.config_helper import get_config_parser
from src.helpers.api_basic_auth_helper import get_api_basic_auth_credentials

api_url_migration = get_config_parser().get("api_url") + '/migration'

def push_beacons():
    beacons = get_beacons.get_beacons()
    _post_beacons_to_api(beacons)

def _post_beacons_to_api(beacons):
    print(f'Printing beacons {_now()}')
    # TODO: update logging once we're actually posting
    # print(f'Posting beacons {_now()}')

    results = []

    for beacon in beacons:
        request_body = get_request_body(beacon)
        _post_beacon(request_body, results)
    
    _print_results_stats(results)
    write_to_csv(results)

def _now():
    return datetime.now()

def _post_beacon(request_body, results):

    # TODO: Post beacon to API and collect response
    # response = requests.post(api_url_migration, json=request_body, auth=get_api_basic_auth_credentials())
    
    # results.append({
    #   'request_body': request_body,
    #   'response_code': response.status_code,
    #   'pk_id': request_body.get('data').get('attributes').get('beacon').get('pkBeaconId')
    #   'api_id': response.json().get('data').get('id') if 'id' in f'{response.content}' else None
    # })

    results.append({
      'request_body': request_body,
      'response_code': 201,
      'pk_id': request_body.get('data').get('attributes').get('beacon').get('pkBeaconId'),
      'api_id': 123
    })


def _print_results_stats(results):
    success = 0
    failure = 0
    for result in results:
        if result.get('status') == 201:
            success += 1
        else:
            failure += 1

    print(f'Stats.  Success: {success}.  Failure: {failure} {_now()}')

if __name__ == '__main__':
  push_beacons()
