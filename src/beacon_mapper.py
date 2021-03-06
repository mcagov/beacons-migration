def get_request_body(beacon):
    return {
        'data': {
            'type': 'legacyBeacon',
            'attributes': {
                'beacon': {
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
                    'createdDate': beacon.get('createDate'),
                    'updateUserId': beacon.get('updateUserId'),
                    'lastModifiedDate': beacon.get('updateDate'),
                    'versioning': beacon.get('versioning'),
                    'note': beacon.get('note'),
                    'manufacturer': beacon.get('manufacturer'),
                    'beaconType': beacon.get('beaconType'),
                    'model': beacon.get('model'),
                    'protocol': beacon.get('protocol'),
                    'mti': beacon.get('mti'),
                    'csta': beacon.get('csta')
                },
                'uses': beacon.get('uses'),
                'owner': beacon.get('owner'),
                'secondaryOwners': beacon.get('secondaryOwners'),
                'emergencyContact': beacon.get('emergencyContact')
            }
        }
    }
