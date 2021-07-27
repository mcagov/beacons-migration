from datetime import datetime, timedelta

from src.aggregate_owners import aggregate_owners


def test_aggregation_of_empty_list():
    assert aggregate_owners([]) == []


def test_no_owners_aggregated():
    now = datetime.now()
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
            'email': 'mca@mcga.gov.uk',
            'created_date': now,
            'last_modified_date': now
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
            'email': 'mca@mcga.gov.uk',
            'created_date': now,
            'last_modified_date': now + timedelta(1)
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
                       'email': 'mca@mcga.gov.uk',
                       'created_date': now,
                       'last_modified_date': now
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
                       'email': 'mca@mcga.gov.uk',
                       'created_date': now,
                       'last_modified_date': now + timedelta(1)
                   }
               }
           ]


def test_two_owners_aggregated():
    now = datetime.now()
    assert aggregate_owners([
        {
            'pk_beacon_owner_id': 1,
            'owner_name': 'Matt',
            'company_name': 'MCA',
            'care_of': 'MCA',
            'address_1': "10 City Beach",
            'address_2': 'Salt Lake',
            'address_3': 'At Home',
            'address_4': 'In Bed',
            'country': 'UK',
            'post_code': 'CL1 2DG',
            'phone_1': '0117123456',
            'phone_2': 'Call me',
            'mobile_1': '07713812678',
            'mobile_2': 'On my mobile',
            'fax': 'Fax me',
            'email': 'mca@mcga.gov.uk',
            'created_date': now,
            'last_modified_date': now
        },
        {
            'pk_beacon_owner_id': 2,
            'owner_name': 'Matt',
            'company_name': 'MCA',
            'care_of': 'MCA',
            'address_1': "10 City Beach",
            'address_2': 'Salt Lake',
            'address_3': 'At Home',
            'address_4': 'In Bed',
            'country': 'UK',
            'post_code': 'CL1 2DG',
            'phone_1': '0117123456',
            'phone_2': 'Call me',
            'mobile_1': '07713812678',
            'mobile_2': 'On my mobile',
            'fax': 'Fax me',
            'email': 'mca@mcga.gov.uk',
            'created_date': now,
            'last_modified_date': now
        }
    ]) == [
               {
                   'pk_keys': {1, 2},
                   'owner': {
                       'owner_name': 'Matt',
                       'company_name': 'MCA',
                       'care_of': 'MCA',
                       'address_1': "10 City Beach",
                       'address_2': 'Salt Lake',
                       'address_3': 'At Home',
                       'address_4': 'In Bed',
                       'country': 'UK',
                       'post_code': 'CL1 2DG',
                       'phone_1': '0117123456',
                       'phone_2': 'Call me',
                       'mobile_1': '07713812678',
                       'mobile_2': 'On my mobile',
                       'fax': 'Fax me',
                       'email': 'mca@mcga.gov.uk',
                       'created_date': now,
                       'last_modified_date': now
                   }
               }
           ]


def test_many_owners_aggregated():
    upper_bound = 100000
    now = datetime.now()
    owner = {'owner_name': 'Matt',
             'company_name': 'MCA',
             'care_of': 'MCA',
             'address_1': "10 City Beach",
             'address_2': 'Salt Lake',
             'address_3': 'At Home',
             'address_4': 'In Bed',
             'country': 'UK',
             'post_code': 'CL1 2DG',
             'phone_1': '0117123456',
             'phone_2': 'Call me',
             'mobile_1': '07713812678',
             'mobile_2': 'On my mobile',
             'fax': 'Fax me',
             'email': 'mca@mcga.gov.uk'
             }
    owners = [{**owner, 'pk_beacon_owner_id': i, 'created_date': now - timedelta(i), 'last_modified_date': now + timedelta(i)} for i in range(0, upper_bound)]
    assert aggregate_owners(owners) == [
        {
            'pk_keys': {i for i in range(0, upper_bound)},
            'owner': {
                **owner,
                'created_date': now - timedelta(upper_bound - 1),
                'last_modified_date': now + timedelta(upper_bound - 1)
            }
        }
    ]


def test_aggregate_owner_with_earliest_created_date():
    now = datetime.now()
    assert aggregate_owners([
        {
            'pk_beacon_owner_id': 1,
            'owner_name': 'Matt',
            'company_name': 'MCA',
            'care_of': 'MCA',
            'address_1': "10 City Beach",
            'address_2': 'Salt Lake',
            'address_3': 'At Home',
            'address_4': 'In Bed',
            'country': 'UK',
            'post_code': 'CL1 2DG',
            'phone_1': '0117123456',
            'phone_2': 'Call me',
            'mobile_1': '07713812678',
            'mobile_2': 'On my mobile',
            'fax': 'Fax me',
            'email': 'mca@mcga.gov.uk',
            'created_date': now,
            'last_modified_date': now
        },
        {
            'pk_beacon_owner_id': 2,
            'owner_name': 'Matt',
            'company_name': 'MCA',
            'care_of': 'MCA',
            'address_1': "10 City Beach",
            'address_2': 'Salt Lake',
            'address_3': 'At Home',
            'address_4': 'In Bed',
            'country': 'UK',
            'post_code': 'CL1 2DG',
            'phone_1': '0117123456',
            'phone_2': 'Call me',
            'mobile_1': '07713812678',
            'mobile_2': 'On my mobile',
            'fax': 'Fax me',
            'email': 'mca@mcga.gov.uk',
            'created_date': now - timedelta(1),
            'last_modified_date': now
        }
    ]) == [
               {
                   'pk_keys': {1, 2},
                   'owner': {
                       'owner_name': 'Matt',
                       'company_name': 'MCA',
                       'care_of': 'MCA',
                       'address_1': "10 City Beach",
                       'address_2': 'Salt Lake',
                       'address_3': 'At Home',
                       'address_4': 'In Bed',
                       'country': 'UK',
                       'post_code': 'CL1 2DG',
                       'phone_1': '0117123456',
                       'phone_2': 'Call me',
                       'mobile_1': '07713812678',
                       'mobile_2': 'On my mobile',
                       'fax': 'Fax me',
                       'email': 'mca@mcga.gov.uk',
                       'created_date': now - timedelta(1),
                       'last_modified_date': now
                   }
               }
           ]


def test_aggregate_owner_with_latest_last_modified_date():
    now = datetime.now()
    assert aggregate_owners([
        {
            'pk_beacon_owner_id': 1,
            'owner_name': 'Matt',
            'company_name': 'MCA',
            'care_of': 'MCA',
            'address_1': "10 City Beach",
            'address_2': 'Salt Lake',
            'address_3': 'At Home',
            'address_4': 'In Bed',
            'country': 'UK',
            'post_code': 'CL1 2DG',
            'phone_1': '0117123456',
            'phone_2': 'Call me',
            'mobile_1': '07713812678',
            'mobile_2': 'On my mobile',
            'fax': 'Fax me',
            'email': 'mca@mcga.gov.uk',
            'created_date': now - timedelta(1),
            'last_modified_date': now + timedelta(1)
        },
        {
            'pk_beacon_owner_id': 2,
            'owner_name': 'Matt',
            'company_name': 'MCA',
            'care_of': 'MCA',
            'address_1': "10 City Beach",
            'address_2': 'Salt Lake',
            'address_3': 'At Home',
            'address_4': 'In Bed',
            'country': 'UK',
            'post_code': 'CL1 2DG',
            'phone_1': '0117123456',
            'phone_2': 'Call me',
            'mobile_1': '07713812678',
            'mobile_2': 'On my mobile',
            'fax': 'Fax me',
            'email': 'mca@mcga.gov.uk',
            'created_date': now - timedelta(1),
            'last_modified_date': now
        }
    ]) == [
               {
                   'pk_keys': {1, 2},
                   'owner': {
                       'owner_name': 'Matt',
                       'company_name': 'MCA',
                       'care_of': 'MCA',
                       'address_1': "10 City Beach",
                       'address_2': 'Salt Lake',
                       'address_3': 'At Home',
                       'address_4': 'In Bed',
                       'country': 'UK',
                       'post_code': 'CL1 2DG',
                       'phone_1': '0117123456',
                       'phone_2': 'Call me',
                       'mobile_1': '07713812678',
                       'mobile_2': 'On my mobile',
                       'fax': 'Fax me',
                       'email': 'mca@mcga.gov.uk',
                       'created_date': now - timedelta(1),
                       'last_modified_date': now + timedelta(1)
                   }
               }
           ]


def test_two_owners_not_aggregated_for_same_values_in_different_fields():
    now = datetime.now()
    assert aggregate_owners([
        {
            'pk_beacon_owner_id': 1,
            'owner_name': 'Matt',
            'company_name': 'MCA',
            'care_of': 'MCA',
            'address_1': "10 City Beach",
            'address_2': 'Salt Lake',
            'address_3': 'At Home',
            'address_4': 'In Bed',
            'country': 'UK',
            'post_code': 'CL1 2DG',
            'phone_1': '0117123456',
            'phone_2': 'Call me',
            'mobile_1': '07713812678',
            'mobile_2': 'On my mobile',
            'fax': 'Fax me',
            'email': 'mca@mcga.gov.uk',
            'created_date': now,
            'last_modified_date': now
        },
        {
            'pk_beacon_owner_id': 2,
            'owner_name': 'Matt',
            'company_name': 'MCA',
            'care_of': 'MCA',
            'address_1': "10 City Beach",
            'address_2': 'Salt Lake',
            'address_3': 'At Home',
            'address_4': 'In Bed',
            'country': 'UK',
            'post_code': 'CL1 2DG',
            'phone_1': '0117123456',
            'phone_2': 'Call me',
            'mobile_1': 'On my mobile',
            'mobile_2': '07713812678',
            'fax': 'Fax me',
            'email': 'mca@mcga.gov.uk',
            'created_date': now,
            'last_modified_date': now
        }
    ]) == [
               {
                   'pk_keys': {1},
                   'owner': {
                       'owner_name': 'Matt',
                       'company_name': 'MCA',
                       'care_of': 'MCA',
                       'address_1': "10 City Beach",
                       'address_2': 'Salt Lake',
                       'address_3': 'At Home',
                       'address_4': 'In Bed',
                       'country': 'UK',
                       'post_code': 'CL1 2DG',
                       'phone_1': '0117123456',
                       'phone_2': 'Call me',
                       'mobile_1': '07713812678',
                       'mobile_2': 'On my mobile',
                       'fax': 'Fax me',
                       'email': 'mca@mcga.gov.uk',
                       'created_date': now,
                       'last_modified_date': now
                   }
               },
               {
                   'pk_keys': {2},
                   'owner': {
                       'owner_name': 'Matt',
                       'company_name': 'MCA',
                       'care_of': 'MCA',
                       'address_1': "10 City Beach",
                       'address_2': 'Salt Lake',
                       'address_3': 'At Home',
                       'address_4': 'In Bed',
                       'country': 'UK',
                       'post_code': 'CL1 2DG',
                       'phone_1': '0117123456',
                       'phone_2': 'Call me',
                       'mobile_1': 'On my mobile',
                       'mobile_2': '07713812678',
                       'fax': 'Fax me',
                       'email': 'mca@mcga.gov.uk',
                       'created_date': now,
                       'last_modified_date': now
                   }
               }
           ]
