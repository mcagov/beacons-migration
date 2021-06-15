import requests
import datetime
import time
import sys
sys.path.append("./helpers")

import config_helper  # noqa
import legacy_database_helper  # noqa

api_url_owner = config_helper.get_config_parser().get(
    "DEVELOPMENT", "api_url") + '/person'


def _postOwner():
    conn = legacy_database_helper.get_db_connection()
    cursor = conn.cursor()
    query = cursor.execute("""
    select * from BEACON_OWNERS_CLEANED where PK_BEACON_OWNER_ID = 24748
        """)
    # Get one row from owner and push to test api
    rows = query.fetchmany()

    if rows == []:
        print("No results found")
        return

    print("Sending dummy owner record to Beacons API: ", api_url_owner)
    for pk_beacon_owner_id, fk_beacon_id, owner_name, company_name, care_of, address_1, address_2, address_3, address_4, country, post_code, phone_1, phone_2, mobile_1, mobile_2, fax, email, is_main, create_user_id, create_dt, update_user_id, update_dt, versioning in rows:
        jsonObj = {"fullName": owner_name, "email": email, "telephoneNumber": phone_1, "alternativeTelephoneNumber": phone_2, "telephoneNumber2": mobile_1, "alternativeTelephoneNumber2": mobile_2, "addressLine1": address_1,
                   "addressLine2": address_2, "addressLine3": address_3, "addressLine4": address_4, "townOrCity": address_3, "postcode": post_code, "country": country, "createdDate": time.mktime(create_dt.timetuple()), "updatedDate": time.mktime(update_dt.timetuple())}
        response = requests.post(api_url_owner, json=jsonObj)

        print("HTTP response status: ", response.status_code)
        # print("Request: ", response.json())

    conn.commit()
    cursor.close()
    conn.close()


_postOwner()
