import sys
import re
import csv

sys.path.append('./helpers')

import config_helper  # noqa
import legacy_database_helper  # noqa

db_connection = legacy_database_helper.get_db_connection()
cursor = db_connection.cursor()

email_regex = '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}'
phone_regex = '[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*'
mobile_regex = '^(\+44\s?7\d{3}|\(?07\d{3}\)?)\s?\d{3}\s?\d{3}$'
postcode_regex = '([A-Z][A-HJ-Y]?\d[A-Z\d]? ?\d[A-Z]{2}|GIR ?0A{2})'
broken_countries = {}


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
    return query.fetchmany()


def _get_valid_emails_list_from_fields(email, phone_1, phone_2, mobile_1, mobile_2):
    valid_emails = []

    if (email != None):
        valid_emails.extend(re.findall(email_regex, email))
    if (phone_1 != None):
        valid_emails.extend(re.findall(email_regex, phone_1))
    if (phone_2 != None):
        valid_emails.extend(re.findall(email_regex, phone_2))
    if (mobile_1 != None):
        valid_emails.extend(re.findall(email_regex, mobile_1))
    if (mobile_2 != None):
        valid_emails.extend(re.findall(email_regex, mobile_2))

    return valid_emails


def _get_valid_phone_numbers_list_from_fields(email, phone_1, phone_2, mobile_1, mobile_2):
    valid_phone_numbers = []

    if (email != None):
        valid_phone_numbers.extend(re.findall(phone_regex, email))
    if (phone_1 != None):
        valid_phone_numbers.extend(re.findall(phone_regex, phone_1))
    if (phone_2 != None):
        valid_phone_numbers.extend(re.findall(phone_regex, phone_2))
    if (mobile_1 != None):
        valid_phone_numbers.extend(re.findall(phone_regex, mobile_1))
    if (mobile_2 != None):
        valid_phone_numbers.extend(re.findall(phone_regex, mobile_2))

    return valid_phone_numbers


def _get_valid_uk_postcode_list_from_fields(address_1, address_2, address_3, address_4, post_code, country):
    uk_postcodes = []

    if (address_1 != None):
        uk_postcodes.extend(re.findall(postcode_regex, address_1))
    if (address_2 != None):
        uk_postcodes.extend(re.findall(postcode_regex, address_2))
    if (address_3 != None):
        uk_postcodes.extend(re.findall(postcode_regex, address_3))
    if (address_4 != None):
        uk_postcodes.extend(re.findall(postcode_regex, address_4))
    if (post_code != None):
        uk_postcodes.extend(re.findall(postcode_regex, post_code))
    if (country != None):
        uk_postcodes.extend(re.findall(postcode_regex, country))

    return uk_postcodes


def _get_valid_uk_mobile_list_from_valid_phone_list(valid_phone_numbers):
    uk_mobiles = []

    for phone_number in valid_phone_numbers:
        if re.fullmatch(mobile_regex, phone_number):
            uk_mobiles.append(phone_number)

    return uk_mobiles


def _get_valid_phone_number_list_from_valid_phone_list(valid_phone_numbers):
    phone_numbers = []

    for phone_number in valid_phone_numbers:
        if re.fullmatch(phone_regex, phone_number):
            phone_numbers.append(phone_number)

    return phone_numbers


def _extract_by_regex(regex, field):
    if field != None:
        # Replace all by regex
        field = re.sub(regex, '', field).strip()
    # return cleaned field
    return field


def _get_broken_countries_dict():
    countries = {}

    with open('./assets/mca_countries.csv') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            correct_country = row['correct_country']
            source_country = row['source_country']
            if correct_country != None or correct_country != '':
                countries[source_country] = correct_country
            else:
                countries[source_country] = source_country

    return countries


def _get_valid_country_from_fields(address_1, address_2, address_3, address_4, post_code, country):
    # Attempt to fix country as we need it for phone number
    valid_country = country
    if valid_country != None and country in broken_countries:
        valid_country = broken_countries[country]
    else:
        # Try to find something that looks like a country elsewhere...
        for field_value in [address_1, address_2, address_3, address_4, post_code]:
            if field_value in broken_countries:
                valid_country = broken_countries[field_value]
                break

    return valid_country


def _set_postcode(post_code, uk_postcodes):
    if len(uk_postcodes) > 0:
        post_code = uk_postcodes[0]
    return post_code


def _set_country(country, valid_country):
    if valid_country != None:
        country = valid_country
    return country


def _set_phone_1(phone_1, other_phone_numbers):
    if len(other_phone_numbers) > 0:
        phone_1 = other_phone_numbers[0]
    return phone_1


def _set_phone_2(phone_2, other_phone_numbers):
    if len(other_phone_numbers) > 1:
        phone_2 = other_phone_numbers[1]
    return phone_2


def _set_mobile_1(mobile_1, uk_mobiles):
    if len(uk_mobiles) > 0:
        mobile_1 = uk_mobiles[0]
    return mobile_1


def _set_mobile_2(phone_2, uk_mobiles):
    if len(uk_mobiles) > 1:
        phone_2 = uk_mobiles[1]
    return phone_2


def _set_email(email, valid_emails):
    if len(valid_emails) > 0:
        email = valid_emails[0].lower()
    return email


def _cleanse_owner_row(pk_beacon_owner_id, fk_beacon_id, owner_name, company_name, care_of, address_1, address_2,
                       address_3, address_4, country, post_code, phone_1, phone_2, mobile_1, mobile_2, fax, email,
                       is_main, create_user_id, create_dt, update_user_id, update_dt, versioning):
    valid_emails = _get_valid_emails_list_from_fields(
        email, phone_1, phone_2, mobile_1, mobile_1)

    email = _extract_by_regex(email_regex, email)
    phone_1 = _extract_by_regex(email_regex, phone_1)
    phone_2 = _extract_by_regex(email_regex, phone_2)
    mobile_1 = _extract_by_regex(email_regex, mobile_1)
    mobile_2 = _extract_by_regex(email_regex, mobile_2)

    print('valid_emails: ', valid_emails)

    valid_phone_numbers = _get_valid_phone_numbers_list_from_fields(
        email, phone_1, phone_2, mobile_1, mobile_1)

    email = _extract_by_regex(phone_regex, email)
    phone_1 = _extract_by_regex(phone_regex, phone_1)
    phone_2 = _extract_by_regex(phone_regex, phone_2)
    mobile_1 = _extract_by_regex(phone_regex, mobile_1)
    mobile_2 = _extract_by_regex(phone_regex, mobile_2)

    print('valid_phone_numbers: ', valid_phone_numbers)

    valid_country = _get_valid_country_from_fields(
        address_1, address_2, address_3, address_4, post_code, country)

    print('valid_country: ', valid_country)

    valid_uk_postcodes = []
    if valid_country == 'UNITED KINGDOM' or valid_country == None:
        valid_uk_postcodes = _get_valid_uk_postcode_list_from_fields(
            address_1, address_2, address_3, address_4, post_code, country)

    print('valid_uk_postcodes: ', valid_uk_postcodes)

    uk_mobiles = _get_valid_uk_mobile_list_from_valid_phone_list(
        valid_phone_numbers)

    print('uk_mobiles: ', uk_mobiles)

    other_phone_numbers = _get_valid_phone_number_list_from_valid_phone_list(
        valid_phone_numbers)

    print('other_phone_numbers: ', other_phone_numbers)

    # Start setting new values

    post_code = _set_postcode(post_code, valid_uk_postcodes)
    country = _set_country(country, valid_country)
    phone_1 = _set_phone_1(phone_1, other_phone_numbers)
    phone_2 = _set_phone_2(phone_2, other_phone_numbers)
    mobile_1 = _set_mobile_1(mobile_1, uk_mobiles)
    mobile_2 = _set_mobile_2(mobile_2, uk_mobiles)
    email = _set_email(email, valid_emails)

    print('Proposed new values:- ', 'email: ', email, ', post_code: ', post_code, ', country: ', country, ', phone_1: ',
          phone_1, ', phone_2: ', phone_2, ', mobile_1: ', mobile_1, ', mobile_2: ', mobile_2)

    # Insert record into DB
    insert_sql = """
            insert into BEACON_OWNERS_CLEANED(
                PK_BEACON_OWNER_ID, FK_BEACON_ID, OWNER_NAME, COMPANY_NAME,
                CARE_OF, ADDRESS_1, ADDRESS_2, ADDRESS_3, ADDRESS_4, COUNTRY, POST_CODE,
                PHONE_1, PHONE_2, MOBILE_1, MOBILE_2, FAX, EMAIL, IS_MAIN, CREATE_USER_ID,
                CREATE_DT, UPDATE_USER_ID, UPDATE_DT, VERSIONING)
                values(:pk_beacon_owner_id, :fk_beacon_id, :owner_name, :company_name, :care_of, :address_1,
                :address_2, :address_3, :address_4, :country, :post_code, :phone_1, :phone_2, :mobile_1, :mobile_2,
                :fax, :email, :is_main, :create_user_id, :create_dt, :update_user_id, :update_dt, :versioning)"""

    insert_cursor = db_connection.cursor()
    insert_cursor.execute(insert_sql,
                          [pk_beacon_owner_id, fk_beacon_id, owner_name, company_name, care_of, address_1, address_2,
                           address_3, address_4,
                           country, post_code, phone_1, phone_2, mobile_1, mobile_2, fax, email, is_main,
                           create_user_id, create_dt, update_user_id, update_dt, versioning])
    insert_cursor.close()


def run_owner_cleansing_rules():
    print('Running through cleansing rules')

    broken_countries = _get_broken_countries_dict()

    _create_clean_owners_table()

    query = cursor.execute("""
        select * from (
            select PK_BEACON_OWNER_ID, FK_BEACON_ID, TRIM(OWNER_NAME), TRIM(COMPANY_NAME),
            TRIM(CARE_OF), TRIM(ADDRESS_1), TRIM(ADDRESS_2), TRIM(
                ADDRESS_3), TRIM(ADDRESS_4), TRIM(COUNTRY), TRIM(POST_CODE),
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

        print("Processing row count: ", len(owners))
        for pk_beacon_owner_id, fk_beacon_id, owner_name, company_name, care_of, address_1, address_2, address_3, address_4, country, post_code, phone_1, phone_2, mobile_1, mobile_2, fax, email, is_main, create_user_id, create_dt, update_user_id, update_dt, versioning in owners:
            _cleanse_owner_row(pk_beacon_owner_id, fk_beacon_id, owner_name, company_name, care_of, address_1,
                               address_2, address_3, address_4, country,
                               post_code, phone_1, phone_2, mobile_1, mobile_2, fax, email, is_main, create_user_id,
                               create_dt, update_user_id, update_dt, versioning)
            i = i + 1
            print('Processing index #: ', i)

            print('Breaking at 100 records, TODO remove later')

    print('Committing and closing db connection')
    db_connection.commit()
    cursor.close()
    db_connection.close()


if __name__ == '__main__':
    run_owner_cleansing_rules()
