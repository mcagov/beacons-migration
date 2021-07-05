from datetime import datetime

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
        matched_owner = hash_to_owners.get(owner_hash, {
            'pk_keys': pk_keys,
            'owner': {
                key: value for key, value in owner.items() if key not in 'pk_beacon_owner_id'
            }
        })
        matched_owner['pk_keys'] |= pk_keys

        hash_to_owners.setdefault(owner_hash, matched_owner)

    print(f'Finished aggregating owners {len(hash_to_owners)} {_now()}')
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


def create_owner_lookup_table():
    print('Creating lookup table')
    with legacy_database_helper.get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(DROP_OWNER_LOOKUP_TABLE_SQL)
            cursor.execute(CREATE_OWNER_LOOKUP_TABLE_SQL)


def post_owners_to_api(owners):
    def post_owner(owner):
        data = {
            'data': {
                'fullName': owner.get('owner_name'),
                'companyName': owner.get('company_name'),
                'careOf': owner.get('care_of'),
                'email': owner.get('email'),
                'telephoneNumber': owner.get('phone_1'),
                'alternativeTelephoneNumber': owner.get('phone_2'),
                'telephoneNumber2': owner.get('mobile_1'),
                'alternativeTelephoneNumber2': owner.get('mobile_2'),
                'fax': owner.get('fax'),
                'isMain': owner.get('is_main'),
                'createUserId': owner.get('create_user_id'),
                'updateUserId': owner.get('update_user_id'),
                'addressLine1': owner.get('address_1'),
                'addressLine2': owner.get('address_2'),
                'addressLine3': owner.get('address_3'),
                'addressLine4': owner.get('address_4'),
                'townOrCity': owner.get('address_3'),
                'postcode': owner.get('post_code'),
                'country': owner.get('country'),
                'createdDate': f'{owner.get("create_dt")}',
                'lastModifiedDate': f'{owner.get("update_dt")}',
                'versioning': owner.get('versioning'),
            }
        }

    print('Posting owners to api')
    result = []


def _now():
    return datetime.now()


if __name__ == '__main__':
    print(f'Starting aggregating owners {_now()}')
    aggregated_owners = get_aggregated_owners()
    create_owner_lookup_table()
    result = post_owners_to_api(aggregated_owners)
