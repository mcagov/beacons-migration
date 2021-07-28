from datetime import datetime
import requests

import src.get_beacons as get_beacons
from src.helpers.config_helper import get_config_parser

api_url_migration = get_config_parser().get("api_url") + '/migration'

def push_beacons():
    beacons = get_beacons.get_beacons()
    _post_beacons_to_api(beacons)

def _post_beacons_to_api(beacons):
    print(f'Printing single beacon {_now()}')
    # TODO: update logging
    # print(f'Posting beacons {_now()}')

    results = []

    for beacon in beacons:
        _post_beacon(beacon, results)
    
    _print_results(results)

def _now():
    return datetime.now()

def _post_beacon(beacon, results):

    body = {
        'type': 'legacyRegistration',
        'data': {
            'attributes': {
                'pkBeaconId': beacon.get('pkBeaconId'),
                'statusCode': beacon.get('statusCode'),
                'isWithdrawn': beacon.get('isWithdrawn'),
                'isPending': beacon.get('isPending'),
                'departRefId': beacon.get('departRefId'),
                'hexId': beacon.get('hexId'),
                'serialNumber': beacon.get('serialNumber'),
                'cospasSarsatNumber': beacon.get('cospasSarsatNumber'),
                'manufacturerSerialNumber': beacon.get('manufacturerSerialNumber'),
                'coding': beacon.get('coding'),
                'firstRegistrationDate': beacon.get('firstRegistrationDate'),
                'lastServiceDate': beacon.get('lastServiceDate'),
                'batteryExpiryDate': beacon.get('batteryExpiryDate'),
                'withdrawnReason': beacon.get('withdrawnReason'),
                'isArchived': beacon.get('isArchived'),
                'createUserId': beacon.get('createUserId'),
                'createDate': beacon.get('createDate'),
                'updateUserId': beacon.get('updateUserId'),
                'updateDate': beacon.get('updateDate'),
                'versioning': beacon.get('versioning'),
                'emergencyContact': beacon.get('emergencyContact'),
                'notes': beacon.get('notes'),
                'uses': beacon.get('uses'),
                'migrated': True,
                'manufacturer': beacon.get('manufacturer'),
                'beaconType': beacon.get('beaconType'),
                'model': beacon.get('model'),
                'protocol': beacon.get('protocol')
            }
        }
    }
    
    print(body)

    # TODO: Post beacon to API and collect response
    # response = requests.post(api_url_migration, json=body)
    # results.append({
    #   'status': response.status_code,
    #   'body': response.content,
    #   'pk_id': beacon.get('pkBeaconId'),
    #   'api_id': response.json().get('data').get('id') if 'id' in f'{response.content}' else None
    # })

def _print_results(results):
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