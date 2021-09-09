import requests
from datetime import datetime

import src.get_beacons as get_beacons
from src.beacon_mapper import get_request_body
from src.helpers.api_basic_auth_helper import get_api_basic_auth_credentials
from src.write_results_to_csv import write_to_csv

from src.helpers.config_helper import get_config_parser

api_url_migration = get_config_parser().get("api_url") + '/migrate/legacy-beacon'


def push_beacons():
    beacons = get_beacons.get_beacons()
    _post_beacons_to_api(beacons)


def _post_beacons_to_api(beacons):
    print(f'Sending {len(beacons)} beacons to the API {_now()}')

    results = []
    count = 0

    for beacon in beacons:
        request_body = get_request_body(beacon)
        _post_beacon(request_body, results)
        count +=1
        if count % 1000 == 0:
            print(f'Sent {count} beacons to the API {_now()}')

    _print_results_stats(results)
    write_to_csv(results)


def _now():
    return datetime.now()


def _post_beacon(request_body, results):
    response = requests.post(api_url_migration, json=request_body, auth=get_api_basic_auth_credentials())

    results.append({
        'response_code': response.status_code,
        'pk_id': request_body.get('data').get('attributes').get('beacon').get('pkBeaconId'),
        'api_id': response.json().get('data', {}).get('id', {}),
        'errors': response.json().get('errors', {}),
        'request_body': request_body
    })


def _print_results_stats(results):
    success = 0
    failure = 0
    for result in results:
        if result.get('response_code') == 201:
            success += 1
        else:
            failure += 1

    print(f'Stats.  Success: {success}.  Failure: {failure} {_now()}')


if __name__ == '__main__':
    push_beacons()
