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
    hash_to_owners = {}

    for owner in owners:
        owner_hash = hash_owner(owner)
        pk_keys = {owner.get('pk_beacon_owner_id')}
        matched_owner = hash_to_owners.get(owner_hash, {
            'pk_keys': pk_keys,
            'owner': {
                key: value for key, value in owner.items() if key not in 'pk_beacon_owner_id'
            }
        })
        matched_owner['pk_keys'] |= pk_keys

        hash_to_owners.setdefault(owner_hash, matched_owner)

    print('Finished aggregating owners', len(hash_to_owners), _now())
    return [aggregated_owner for aggregated_owner in hash_to_owners.values()]


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
