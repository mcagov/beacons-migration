import os
import cx_Oracle
import re
import csv

cx_Oracle.init_oracle_client(lib_dir=os.environ.get("HOME")+"/instantclient_19_8")

def _getDBConnection():
    conn = cx_Oracle.connect(
        user="system",
        password="oracle",
        dsn="localhost/XE")
    # Set to desired Oracle schema
    conn.current_schema = 'CERSSVD_SCHEMA'
    print("Successfully connected to Oracle Database")
    return conn

def _postOwners():
    conn = _getDBConnection()
    cursor = conn.cursor()
    query = cursor.execute("""
    select * from BEACON_OWNERS_CLEANED
        order by CREATE_DT DESC)
        """)
    # Dummy loop here, using query.fetchmany() each time to return a bunch of rows.
    while True:
        rows = query.fetchmany()
        if rows == []:
            # No more results
            break
        for pk_beacon_owner_id, fk_beacon_id, owner_name, company_name, care_of, address_1, address_2, address_3, address_4, country, post_code, phone_1, phone_2, mobile_1, mobile_2, fax, email, is_main, create_user_id, create_dt, update_user_id, update_dt, versioning in rows:
           response = requests.post(os.getenv('API_URL'), json={'owner_name': owner_name, 'owner_email': email})

           print("Status: ", response.status_code)
           print("Request: ", response.json())
    conn.commit()
    cursor.close()
    conn.close()


# Clean Owners...
_postOwners()