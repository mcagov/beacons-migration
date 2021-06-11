import os
import sys
import re
sys.path.append('./helpers')


import config_helper  # noqa
import legacy_database_helper  # noqa

db_connection = legacy_database_helper.get_db_connection()
cursor = db_connection.cursor()

email_regex = '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}'


def _print_affected_rows(cursor):
    print('Affected rows: ', cursor.rowcount)


def _create_clean_owners_table():
    cursor.execute("""
        begin
            execute immediate 'drop table BEACON_OWNERS_CLEANED';
            exception when others then if sqlcode <> -942 then raise; end if;
        end;""")
    cursor.execute(
        """CREATE TABLE BEACON_OWNERS_CLEANED AS SELECT * FROM BEACON_OWNERS WHERE 1=0""")
    _print_affected_rows(cursor)


def _get_batch_of_owners(query):
    rows = query.fetchmany()
    return rows


def _extract_by_regex(regex, field, target_array):
    if field != None:
        # Extract all by regex
        target_array.extend(re.findall(regex, field))
        # Replace all by regex
        field = re.sub(regex, '', field).strip()
    # return cleaned field
    return field, target_array


def _cleanse_owner_email(email, valid_emails):
    return _extract_by_regex(email_regex, email, valid_emails)


def _cleanse_owner_phone_1(phone_1, valid_emails):
    return _extract_by_regex(email_regex, phone_1, valid_emails)


def _cleanse_owner_phone_2(phone_2, valid_emails):
    return _extract_by_regex(email_regex, phone_2, valid_emails)


def _cleanse_owner_mobile_1(mobile_1, valid_emails):
    return _extract_by_regex(email_regex, mobile_1, valid_emails)


def _cleanse_owner_mobile_2(mobile_2, valid_emails):
    return _extract_by_regex(email_regex, mobile_2, valid_emails)


def _cleanse_owner_row(pk_beacon_owner_id, fk_beacon_id, owner_name, company_name, care_of, address_1, address_2, address_3, address_4, country, post_code, phone_1, phone_2, mobile_1, mobile_2, fax, email, is_main, create_user_id, create_dt, update_user_id, update_dt, versioning):
    valid_emails = []
    email, valid_emails = _cleanse_owner_email(email, valid_emails)
    phone_1, valid_emails = _cleanse_owner_phone_1(phone_1, valid_emails)
    phone_2, valid_emails = _cleanse_owner_phone_2(phone_2, valid_emails)
    mobile_1, valid_emails = _cleanse_owner_mobile_1(mobile_1, valid_emails)
    mobile_2, valid_emails = _cleanse_owner_mobile_2(mobile_2, valid_emails)

    print('valid_emails: ', valid_emails)
    # HERE


def _run_rules():
    print('Running through cleansing rules')

    _create_clean_owners_table()

    query = cursor.execute("""
        select * from (
            select PK_BEACON_OWNER_ID, FK_BEACON_ID, TRIM(OWNER_NAME), TRIM(COMPANY_NAME),
            TRIM(CARE_OF), TRIM(ADDRESS_1), TRIM(ADDRESS_2), TRIM(ADDRESS_3), TRIM(ADDRESS_4), TRIM(COUNTRY), TRIM(POST_CODE),
            PHONE_1, PHONE_2, MOBILE_1, MOBILE_2, FAX, EMAIL, IS_MAIN, CREATE_USER_ID,
            CREATE_DT, UPDATE_USER_ID, UPDATE_DT, VERSIONING
            from BEACON_OWNERS
            order by CREATE_DT DESC)
            """)

    i = 0

    while True:

        owners = _get_batch_of_owners(query)

        if owners == []:
            # No more results
            print("No more owner records found")
            break

        for pk_beacon_owner_id, fk_beacon_id, owner_name, company_name, care_of, address_1, address_2, address_3, address_4, country, post_code, phone_1, phone_2, mobile_1, mobile_2, fax, email, is_main, create_user_id, create_dt, update_user_id, update_dt, versioning in owners:
            _cleanse_owner_row(pk_beacon_owner_id, fk_beacon_id, owner_name, company_name, care_of, address_1, address_2, address_3, address_4, country,
                               post_code, phone_1, phone_2, mobile_1, mobile_2, fax, email, is_main, create_user_id, create_dt, update_user_id, update_dt, versioning)

        i = i + 1

        if i == 100:
            print('Breaking at 100 records, TODO remove later')
            break

    cursor.close()
    db_connection.close()


_run_rules()
