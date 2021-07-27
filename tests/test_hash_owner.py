from src.aggregate_owners import hash_owner


def test_hash_owner_is_a_match_for_the_same_user():
    owner = {'pk_beacon_owner_id': 1,
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
             'email': 'mca@mcga.gov.uk'}
    assert hash_owner(owner) == hash_owner(owner)


def test_hash_owner_is_a_match_for_the_same_user_with_none_values():
    owner = {'pk_beacon_owner_id': 1,
             'owner_name': 'Matt',
             'company_name': None,
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
             'email': 'mca@mcga.gov.uk'}
    assert hash_owner(owner) == hash_owner(owner)


def test_hash_owner_is_not_a_match_with_same_owner_information_but_in_different_fields():
    owner = {'pk_beacon_owner_id': 1,
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
             'email': 'mca@mcga.gov.uk'}

    owner_to_compare = {'pk_beacon_owner_id': 2,
                        'owner_name': 'MCA',
                        'company_name': 'Matt',
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
                        'email': 'mca@mcga.gov.uk'}
    assert hash_owner(owner) != hash_owner(owner_to_compare)


def test_hash_owner_is_not_a_match_for_case_values_in_different_casing():
    owner = {'pk_beacon_owner_id': 1,
             'owner_name': 'Matt',
             'company_name': None,
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
             'email': 'mca@mcga.gov.uk'}

    to_compare = {'pk_beacon_owner_id': 1,
             'owner_name': 'matt',
             'company_name': None,
             'care_of': 'mca',
             'address_1': "10 City Beach",
             'address_2': 'salt lake',
             'address_3': 'At Home',
             'address_4': 'In Bed',
             'country': 'UK',
             'post_code': 'CL1 2DG',
             'phone_1': '0117123456',
             'phone_2': 'Call me',
             'mobile_1': '07713812678',
             'mobile_2': 'On my mobile',
             'fax': 'Fax me',
             'email': 'mca@mcga.gov.uk'}
    assert hash_owner(owner) != hash_owner(to_compare)

