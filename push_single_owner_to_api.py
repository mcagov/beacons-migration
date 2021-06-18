import requests
import datetime
import time
import sys
sys.path.append("./helpers")

import config_helper  # noqa
import legacy_database_helper  # noqa

api_url_owner = config_helper.get_config_parser().get(
    "LOCAL", "api_url") + '/person'


def _postOwner():
    conn = legacy_database_helper.get_db_connection()
    cursor = conn.cursor()
    query = cursor.execute("""
    select * from BEACON_OWNERS_CLEANED where PK_BEACON_OWNER_ID = 228395
        """)
    # Get one row from owner and push to test api
    rows = query.fetchmany()

    if rows == []:
        print("No results found")
        return

    print("Sending dummy owner record to Beacons API: ", api_url_owner)
    for pk_beacon_owner_id, fk_beacon_id, owner_name, company_name, care_of, address_1, address_2, address_3, address_4, country, post_code, phone_1, phone_2, mobile_1, mobile_2, fax, email, is_main, create_user_id, create_dt, update_user_id, update_dt, versioning in rows:
        dataJsonObj = {
            "data": {
                "attributes": {
                    "fullName": owner_name,
                    "companyName": company_name,
                    "careOf": care_of,
                    "email": email,
                    "telephoneNumber": phone_1,
                    "alternativeTelephoneNumber": phone_2,
                    "telephoneNumber2": mobile_1,
                    "alternativeTelephoneNumber2": mobile_2,
                    "fax": fax,
                    "isMain": is_main,
                    "createUserId": create_user_id,
                    "updateUserId": update_user_id,
                    "addressLine1": address_1,
                    "addressLine2": address_2,
                    "addressLine3": address_3,
                    "addressLine4": address_4,
                    "townOrCity": address_3,
                    "postcode": post_code,
                    "country": country,
                    "createdDate": str(create_dt),
                    "LastModifiedDate": str(update_dt),
                    "versioning": versioning,
                    "personType": "OWNER"
                }
            }
        }
        response = requests.post(api_url_owner, json=dataJsonObj)

        print("HTTP response status: ", response.status_code)
        # print("Request: ", response.json())

    conn.commit()
    cursor.close()
    conn.close()


_postOwner()
