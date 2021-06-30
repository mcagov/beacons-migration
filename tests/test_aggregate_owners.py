"""
Row from the DB:

pk_beacon_owner_id,
fk_beacon_id, ❌
owner_name,
company_name,
care_of,
address_1,
address_2,
address_3,
address_4,
country,
post_code,
phone_1,
phone_2,
mobile_1,
mobile_2,
fax,
email,
is_main, ❌
create_user_id, ❌
create_dt, ❌
update_user_id, ❌
update_dt, ❌
versioning ❌

"""
from etl.aggregate_owners import aggregate_owners


def test_aggregation_of_empty_list():
    assert aggregate_owners([]) == []


def test_no_users_aggregated():
    assert aggregate_owners([
        {
            'pk_beacon_owner_id': 1,
            'owner_name': 'Matt',
            'company_name': 'MCA',
            'care_of': 'MCA',
            'address_1': "10 City Beach",
            'address_2': None,
            'address_3': None,
            'address_4': None,
            'country': 'UK',
            'post_code': 'CL1 2DG',
            'phone_1': '0117123456',
            'phone_2': None,
            'mobile_1': '07713812678',
            'mobile_2': None,
            'fax': None,
            'email': 'mca@mcga.gov.uk'
        },
        {
            'pk_beacon_owner_id': 2,
            'owner_name': 'Zack',
            'company_name': 'MCA',
            'care_of': 'MCA',
            'address_1': "10 City Beach",
            'address_2': None,
            'address_3': None,
            'address_4': None,
            'country': 'UK',
            'post_code': 'CL1 2DG',
            'phone_1': '0117123456',
            'phone_2': None,
            'mobile_1': '07713812678',
            'mobile_2': None,
            'fax': None,
            'email': 'mca@mcga.gov.uk'
        }
    ]) == [
               {
                   'pk_keys': {1},
                   'owner': {
                       'owner_name': 'Matt',
                       'company_name': 'MCA',
                       'care_of': 'MCA',
                       'address_1': "10 City Beach",
                       'address_2': None,
                       'address_3': None,
                       'address_4': None,
                       'country': 'UK',
                       'post_code': 'CL1 2DG',
                       'phone_1': '0117123456',
                       'phone_2': None,
                       'mobile_1': '07713812678',
                       'mobile_2': None,
                       'fax': None,
                       'email': 'mca@mcga.gov.uk'
                   }
               },
               {
                   'pk_keys': {2},
                   'owner': {
                       'owner_name': 'Zack',
                       'company_name': 'MCA',
                       'care_of': 'MCA',
                       'address_1': "10 City Beach",
                       'address_2': None,
                       'address_3': None,
                       'address_4': None,
                       'country': 'UK',
                       'post_code': 'CL1 2DG',
                       'phone_1': '0117123456',
                       'phone_2': None,
                       'mobile_1': '07713812678',
                       'mobile_2': None,
                       'fax': None,
                       'email': 'mca@mcga.gov.uk'
                   }
               }
           ]
