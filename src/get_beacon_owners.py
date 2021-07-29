import src.helpers.legacy_database_helper as legacy_database_helper
from src.helpers.date_helper import get_isoformat

db_connection = legacy_database_helper.get_db_connection()
cursor = db_connection.cursor()

def get_owners(beacon_id):
  owners = _get_owner_rows(beacon_id)

  results = []

  for pk_beacon_owner_id, fk_beacon_id, owner_name, company_name, care_of, \
    address_1, address_2, address_3, address_4, country, post_code, phone_1, \
    phone_2, mobile_1, mobile_2, fax, email, is_main, create_user_id, \
    create_dt, update_user_id, update_dt, versioning in owners:
      
      results.append({
          'pkBeaconOwnerId': pk_beacon_owner_id,
          'fkBeaconId': fk_beacon_id,
          'ownerName': owner_name,
          'companyName': company_name,
          'careOf': care_of,
          'address1': address_1,
          'address2': address_2,
          'address3': address_3,
          'address4': address_4,
          'country': country,
          'postCode': post_code,
          'phone1': phone_1,
          'phone2': phone_2,
          'mobile1': mobile_1,
          'mobile2': mobile_2,
          'fax': fax,
          'email': email,
          'isMain': is_main,
          'createUserId': create_user_id,
          'createDt': get_isoformat(create_dt),
          'updateUserId': update_user_id,
          'updateDt': get_isoformat(update_dt),
          'versioning': versioning
      })

  return results

def _get_owner_rows(beacon_id):
  query = cursor.execute(f"""
  SELECT * FROM BEACON_OWNERS_CLEANED
  WHERE FK_BEACON_ID='{beacon_id}'
  """)

  return query.fetchall()
