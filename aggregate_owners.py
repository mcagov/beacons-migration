from datetime import datetime

from helpers import legacy_database_helper

GET_ALL_OWNERS_QUERY = "SELECT * FROM BEACON_OWNERS_CLEANED ORDER BY CREATE_DT DESC"


def post_aggregated_owners():
    print('Starting aggregating owners', _now())
    aggregated_owners = get_aggregated_owners()
    print('Number of aggregated owners:', len(aggregated_owners), _now())


def get_aggregated_owners():
    owner_rows = get_owner_rows()
    return aggregate_owners(owner_rows)


def get_owner_rows():
    print('Getting owner rows', _now())
    result = []

    conn = legacy_database_helper.get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute(GET_ALL_OWNERS_QUERY)
        rows = cursor.fetchall()
        for pk_beacon_owner_id, fk_beacon_id, owner_name, company_name, care_of, address_1, address_2, address_3, address_4, country, post_code, phone_1, phone_2, mobile_1, mobile_2, fax, email, is_main, create_user_id, create_dt, update_user_id, update_dt, versioning in rows:
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
                'email': email
            })

    print(f'Finished extracting owner rows.  Number of rows: {len(result)}.  Matched owners: {len(result)}', _now())
    return result


def aggregate_owners(owners):
    print('Starting to aggregate owners', len(owners), _now())
    count = 0
    result = {}

    for owner in owners:
        count += 1
        owner_hash = hash_owner(owner)
        pk_keys = {owner.get('pk_beacon_owner_id')}
        matched_owner = result.get(owner_hash, {
            'pk_keys': pk_keys,
            'owner': {
                key: value for key, value in owner.items() if key not in 'pk_beacon_owner_id'
            }
        })
        matched_owner['pk_keys'] |= pk_keys

        if count % 100000 == 0:
            print(f'Compared {count} owners {_now()}.  Number of duplicates {len(result)}')

    print('Finished aggregating owners', len(result), _now())
    return result.values()


def _is_same_owner(owner, to_compare):
    return (owner.get('owner_name') == to_compare.get('owner_name')) and \
           (owner.get('company_name') == to_compare.get('company_name')) and \
           (owner.get('care_of') == to_compare.get('care_of')) and \
           (owner.get('address_1') == to_compare.get('address_1')) and \
           (owner.get('address_2') == to_compare.get('address_2')) and \
           (owner.get('address_3') == to_compare.get('address_3')) and \
           (owner.get('address_4') == to_compare.get('address_4')) and \
           (owner.get('country') == to_compare.get('country')) and \
           (owner.get('post_code') == to_compare.get('post_code')) and \
           (owner.get('phone_1') == to_compare.get('phone_1')) and \
           (owner.get('phone_2') == to_compare.get('phone_2')) and \
           (owner.get('mobile_1') == to_compare.get('mobile_1')) and \
           (owner.get('mobile_2') == to_compare.get('mobile_2')) and \
           (owner.get('fax') == to_compare.get('fax')) and \
           (owner.get('email') == to_compare.get('email'))


def hash_owner(owner):
    return f'{hash(owner.get("owner_name"))}-{hash(owner.get("company_name"))}-' + \
           f'{hash(owner.get("care_of"))}-{hash(owner.get("address_1"))}-' + \
           f'{hash(owner.get("address_2"))}-{hash(owner.get("address_3"))}-' + \
           f'{hash(owner.get("address_4"))}-{hash(owner.get("country"))}-' + \
           f'{hash(owner.get("post_code"))}-{hash(owner.get("phone_1"))}-' + \
           f'{hash(owner.get("phone_2"))}-{hash(owner.get("mobile_1"))}-' + \
           f'{hash(owner.get("mobile_2"))}-{hash(owner.get("fax"))}-' + \
           f'{hash(owner.get("email"))}'


def _now():
    return datetime.now()


if __name__ == '__main__':
    print('aggregating owners, might take some time')
    post_aggregated_owners()
