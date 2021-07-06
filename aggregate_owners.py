from datetime import datetime
from functools import reduce

import requests

from helpers import legacy_database_helper
from helpers.config_helper import get_config_parser

GET_ALL_OWNERS_QUERY = "SELECT * FROM BEACON_OWNERS_CLEANED ORDER BY CREATE_DT DESC"
DROP_OWNER_LOOKUP_TABLE_SQL = """
begin
    execute immediate 'drop table BEACON_OWNERS_LOOKUP';
    exception when others then if sqlcode <> -942 then raise; end if;
end;
"""
CREATE_OWNER_LOOKUP_TABLE_SQL = "CREATE TABLE BEACON_OWNERS_LOOKUP (PK_BEACON_OWNER_ID NUMBER(28), API_ID VARCHAR(36))"

api_url_owner = get_config_parser().get(
    "LOCAL", "api_url") + '/owner'


def get_aggregated_owners():
    owner_rows = get_owner_rows()
    return aggregate_owners(owner_rows)


def get_owner_rows():
    print(f'Getting owner rows {_now()}')
    result = []

    with legacy_database_helper.get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(GET_ALL_OWNERS_QUERY)
            rows = cursor.fetchall()
            for pk_beacon_owner_id, fk_beacon_id, owner_name, company_name, care_of, address_1, address_2, address_3, \
                address_4, country, post_code, phone_1, phone_2, mobile_1, mobile_2, fax, email, \
                is_main, create_user_id, create_dt, update_user_id, update_dt, versioning in rows:
                result.append({
                    'pk_beacon_owner_id': pk_beacon_owner_id,
                    'owner_name': owner_name,
                    'company_name': company_name,
                    'care_of': care_of,
                    'address_1': address_1,
                    'address_2': address_2,
                    'address_3': address_3,
                    'address_4': address_4,
                    'country': country,
                    'post_code': post_code,
                    'phone_1': phone_1,
                    'phone_2': phone_2,
                    'mobile_1': mobile_1,
                    'mobile_2': mobile_2,
                    'fax': fax,
                    'email': email,
                    'created_date': create_dt,
                    'last_modified_date': update_dt
                })

    print(f'Finished extracting owner rows.  Number of rows {len(result)}.  Matched owners: {len(result)}', _now())
    return result


def aggregate_owners(owners):
    print(f'Starting to aggregate owners {len(owners)} {_now()}')
    hash_to_owners = {}

    for owner in owners:
        owner_hash = hash_owner(owner)
        pk_keys = {owner.get('pk_beacon_owner_id')}
        created_dates = [owner.get('created_date')]
        last_modified_dates = [owner.get('last_modified_date')]
        matched_owner = hash_to_owners.get(owner_hash, {
            'pk_keys': pk_keys,
            'owner': {
                key: value for key, value in owner.items() if key not in ['pk_beacon_owner_id', 'created_date', 'last_modified_dates']
            },
            'created_dates': created_dates,
            'last_modified_dates': last_modified_dates
        })
        matched_owner['pk_keys'] |= pk_keys
        matched_owner['created_dates'] += created_dates
        matched_owner['owner']['created_date'] = earliest_date(matched_owner.get('created_dates'))
        matched_owner['owner']['last_modified_date'] = latest_date(matched_owner.get('last_modified_dates'))

        hash_to_owners.setdefault(owner_hash, matched_owner)

    print(f'Finished aggregating owners {len(hash_to_owners)} {_now()}')
    return [{k: v for k, v in owner.items() if k not in ['created_dates', 'last_modified_dates']} for owner in hash_to_owners.values()]


def hash_owner(owner):
    return f'{hash(owner.get("owner_name"))}-{hash(owner.get("company_name"))}-' + \
           f'{hash(owner.get("care_of"))}-{hash(owner.get("address_1"))}-' + \
           f'{hash(owner.get("address_2"))}-{hash(owner.get("address_3"))}-' + \
           f'{hash(owner.get("address_4"))}-{hash(owner.get("country"))}-' + \
           f'{hash(owner.get("post_code"))}-{hash(owner.get("phone_1"))}-' + \
           f'{hash(owner.get("phone_2"))}-{hash(owner.get("mobile_1"))}-' + \
           f'{hash(owner.get("mobile_2"))}-{hash(owner.get("fax"))}-' + \
           f'{hash(owner.get("email"))}'


def earliest_date(dates):
    filtered_dates = [date for date in dates if date is not None]
    filtered_dates.sort()
    return filtered_dates[0]


def latest_date(dates):
    filtered_dates = [date for date in dates if date is not None]
    filtered_dates.sort()
    return filtered_dates[-1]


def create_owner_lookup_table():
    print('Creating lookup table')
    with legacy_database_helper.get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(DROP_OWNER_LOOKUP_TABLE_SQL)
            cursor.execute(CREATE_OWNER_LOOKUP_TABLE_SQL)


def post_owners_to_api(owners):
    def post_owner(o):
        owner_details = o.get('owner')
        data = {
            'data': {
                'fullName': owner_details.get('owner_name'),
                'companyName': owner_details.get('company_name'),
                'careOf': owner_details.get('care_of'),
                'email': owner_details.get('email'),
                'telephoneNumber': owner_details.get('phone_1'),
                'alternativeTelephoneNumber': owner_details.get('phone_2'),
                'telephoneNumber2': owner_details.get('mobile_1'),
                'alternativeTelephoneNumber2': owner_details.get('mobile_2'),
                'fax': owner_details.get('fax'),
                'isMain': owner_details.get('is_main'),
                'createUserId': owner_details.get('create_user_id'),
                'updateUserId': owner_details.get('update_user_id'),
                'addressLine1': owner_details.get('address_1'),
                'addressLine2': owner_details.get('address_2'),
                'addressLine3': owner_details.get('address_3'),
                'addressLine4': owner_details.get('address_4'),
                'townOrCity': owner_details.get('address_3'),
                'postcode': owner_details.get('post_code'),
                'country': owner_details.get('country'),
                'createdDate': f'{owner_details.get("create_dt")}',
                'lastModifiedDate': f'{owner_details.get("update_dt")}'
            }
        }

        response = requests.post(api_url_owner, json=data)
        results.append({
            'status': response.status_code,
            'body': response.json(),
            'pk_keys': owner.get('pk_keys')
        })

    results = []

    for owner in owners:
        post_owner(owner)

    print(f'Posted {len(results)} owners')

    return results


def _now():
    return datetime.now()


if __name__ == '__main__':
    print(f'Starting aggregating owners {_now()}')
    aggregated_owners = get_aggregated_owners()
    create_owner_lookup_table()
    results = post_owners_to_api(aggregated_owners)
