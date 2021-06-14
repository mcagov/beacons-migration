import os
import cx_Oracle
import re
import csv

cx_Oracle.init_oracle_client(
    lib_dir=os.environ.get("HOME")+"/instantclient_19_8")


def _getDBConnection():
    conn = cx_Oracle.connect(
        user="system",
        password="oracle",
        dsn="localhost/XE")
    # Set to desired Oracle schema
    conn.current_schema = 'CERSSVD_SCHEMA'
    print("Successfully connected to Oracle Database")
    return conn


"""
This is horrible ... I made a CSV of all the terrible country mistakes and mapped them to real countries.
We should align this to whatever country list we're using on the front end.
 """


def _getBrokenCountriesDict():
    countries = {}
    with open('mca_countries.csv') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            correct_country = row['correct_country']
            source_country = row['source_country']
            if correct_country != None or correct_country != '':
                countries[source_country] = correct_country
            else:
                countries[source_country] = source_country

    return countries


def _createCleanOwnersTable():
    connection = _getDBConnection()
    cursor = connection.cursor()
    cursor.execute("""
        begin
            execute immediate 'drop table BEACON_OWNERS_CLEANED';
            exception when others then if sqlcode <> -942 then raise; end if;
        end;""")
    cursor.execute(
        """CREATE TABLE BEACON_OWNERS_CLEANED AS SELECT * FROM BEACON_OWNERS WHERE 1=0""")
    cursor.close()
    connection.close()


"""
Helper method to extract based on a regex
 """


def _extractByRegex(regex, field, target_array):
    if field != None:
        # Extract all by regex
        target_array.extend(re.findall(regex, field))
        # Replace all by regex
        field = re.sub(regex, '', field).strip()
    # return cleaned field
    return field


"""
Get all exisitng main owners, clean each record and write back to new table.
For analysis purposes I didn't care whether addresses were correct - I was mainly
trying to get data in the right columns so look at feasibility of aggregation and
how many owners we could contact via SMS/email.
"""


def _cleanOwners():
    _createCleanOwnersTable()
    conn = _getDBConnection()
    cursor = conn.cursor()
    broken_countries = _getBrokenCountriesDict()
    query = cursor.execute("""
    select * from (
        select PK_BEACON_OWNER_ID, FK_BEACON_ID, TRIM(OWNER_NAME), TRIM(COMPANY_NAME),
        TRIM(CARE_OF), TRIM(ADDRESS_1), TRIM(ADDRESS_2), TRIM(ADDRESS_3), TRIM(ADDRESS_4), TRIM(COUNTRY), TRIM(POST_CODE),
        PHONE_1, PHONE_2, MOBILE_1, MOBILE_2, FAX, EMAIL, IS_MAIN, CREATE_USER_ID,
        CREATE_DT, UPDATE_USER_ID, UPDATE_DT, VERSIONING
        from BEACON_OWNERS
        order by CREATE_DT DESC)
        """)
    # Dummy loop here, using query.fetchmany() each time to return a bunch of rows.
    while True:
        rows = query.fetchmany()
        if rows == []:
            # No more results
            break
        for pk_beacon_owner_id, fk_beacon_id, owner_name, company_name, care_of, address_1, address_2, address_3, address_4, country, post_code, phone_1, phone_2, mobile_1, mobile_2, fax, email, is_main, create_user_id, create_dt, update_user_id, update_dt, versioning in rows:
            # Try to find all emails (we need to look in many fields for these!)...
            email_regex = '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}'
            valid_emails = []
            email = _extractByRegex(email_regex, email, valid_emails)
            phone_1 = _extractByRegex(email_regex, phone_1, valid_emails)
            phone_2 = _extractByRegex(email_regex, phone_2, valid_emails)
            mobile_1 = _extractByRegex(email_regex, mobile_1, valid_emails)
            mobile_2 = _extractByRegex(email_regex, mobile_2, valid_emails)

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
            # Try to find a postcode - If I don't have a country I assume it's UK :-/
            uk_postcodes = []
            if valid_country == 'UNITED KINGDOM' or valid_country == None:
                postcode_regex = '([A-Z][A-HJ-Y]?\d[A-Z\d]? ?\d[A-Z]{2}|GIR ?0A{2})'
                post_code = _extractByRegex(
                    postcode_regex, post_code, uk_postcodes)
                country = _extractByRegex(
                    postcode_regex, country, uk_postcodes)
                address_4 = _extractByRegex(
                    postcode_regex, address_4, uk_postcodes)
                address_3 = _extractByRegex(
                    postcode_regex, address_3, uk_postcodes)
                address_2 = _extractByRegex(
                    postcode_regex, address_2, uk_postcodes)
                address_1 = _extractByRegex(
                    postcode_regex, address_1, uk_postcodes)

            # Try to find all phone numbers - regex is not perfect but good enough for this.
            phone_regex = '[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*'
            valid_phone_numbers = []
            phone_1 = _extractByRegex(
                phone_regex, phone_1, valid_phone_numbers)
            phone_2 = _extractByRegex(
                phone_regex, phone_2, valid_phone_numbers)
            mobile_1 = _extractByRegex(
                phone_regex, mobile_1, valid_phone_numbers)
            mobile_2 = _extractByRegex(
                phone_regex, mobile_2, valid_phone_numbers)
            email = _extractByRegex(phone_regex, email, valid_phone_numbers)
            # Split into UK mobile and other - regex seems to be pretty reliable.
            mobile_regex = '^(\+44\s?7\d{3}|\(?07\d{3}\)?)\s?\d{3}\s?\d{3}$'
            uk_mobiles = []
            other_phone_numbers = []
            for phone_number in valid_phone_numbers:
                if re.fullmatch(mobile_regex, phone_number):
                    uk_mobiles.append(phone_number)
                elif re.fullmatch(phone_regex, phone_number):
                    other_phone_numbers.append(phone_number)

            #print({'country': valid_country, 'emails': valid_emails, 'uk_mobiles:': uk_mobiles, 'phone_numbers': other_phone_numbers, 'uk_postcodes': uk_postcodes})

            # Now set fields
            if (valid_country == 'UNITED KINGDOM' or valid_country == None) and len(uk_postcodes) > 0:
                post_code = uk_postcodes[0]
            if valid_country != None:
                country = valid_country
            phone_1 = None
            phone_2 = None
            mobile_1 = None
            mobile_2 = None
            if len(uk_mobiles) > 0:
                mobile_1 = uk_mobiles[0]
                if len(uk_mobiles) > 1:
                    mobile_2 = uk_mobiles[1]
            if len(other_phone_numbers) > 0:
                phone_1 = other_phone_numbers[0]
                if len(other_phone_numbers) > 1:
                    phone_2 = other_phone_numbers[1]
            if len(valid_emails) > 0:
                email = valid_emails[0].lower()
            else:
                email = None
            insert_sql = """
            insert into BEACON_OWNERS_CLEANED(
                PK_BEACON_OWNER_ID, FK_BEACON_ID, OWNER_NAME, COMPANY_NAME,
                CARE_OF, ADDRESS_1, ADDRESS_2, ADDRESS_3, ADDRESS_4, COUNTRY, POST_CODE,
                PHONE_1, PHONE_2, MOBILE_1, MOBILE_2, FAX, EMAIL, IS_MAIN, CREATE_USER_ID,
                CREATE_DT, UPDATE_USER_ID, UPDATE_DT, VERSIONING)
                values(:pk_beacon_owner_id, :fk_beacon_id, :owner_name, :company_name, :care_of, :address_1,
                :address_2, :address_3, :address_4, :country, :post_code, :phone_1, :phone_2, :mobile_1, :mobile_2,
                :fax, :email, :is_main, :create_user_id, :create_dt, :update_user_id, :update_dt, :versioning)"""
            insert_cursor = conn.cursor()
            insert_cursor.execute(insert_sql, [pk_beacon_owner_id, fk_beacon_id, owner_name, company_name, care_of, address_1, address_2, address_3, address_4,
                                  country, post_code, phone_1, phone_2, mobile_1, mobile_2, fax, email, is_main, create_user_id, create_dt, update_user_id, update_dt, versioning])
            insert_cursor.close()

    conn.commit()
    cursor.close()
    conn.close()


# Clean Owners...
_cleanOwners()
