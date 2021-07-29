import src.get_beacon_uses as get_beacon_uses
import src.helpers.date_helper as date_helper
import src.helpers.legacy_database_helper as legacy_database_helper

db_connection = legacy_database_helper.get_db_connection()
cursor = db_connection.cursor()

GET_ALL_BEACONS_QUERY = "SELECT * FROM BEACONS"

def get_beacons():
    results = []

    beacons = _get_beacon_rows()
    
    for pk_beacon_id, status_code, is_withdrawn, is_pending, depart_ref_id, \
        hex_id, serial_no, cospas_sarsat_no, fk_mti_code, fk_csta_code, \
        fk_model_code, fk_protocol_type_id, fk_beacon_type_code, \
        fk_manufacturer_id, manufacturer_serial_no, coding, \
        first_registration_dt, last_service_date, battery_expiry_date, \
        emergency_contact, withdrawn_reason, note, is_archived, create_user_id, \
        create_dt, update_user_id, update_dt, versioning,  in beacons:

        uses = get_beacon_uses.get_uses(pk_beacon_id)

        results.append({
            'pkBeaconId': pk_beacon_id,
            'statusCode': status_code,
            'isWithdrawn': is_withdrawn,
            'isPending': is_pending,
            'departRefId': depart_ref_id,
            'hexId': hex_id,
            'serialNumber': serial_no,
            'cospasSarsatNumber': cospas_sarsat_no,
            'manufacturerSerialNumber': manufacturer_serial_no,
            'coding': coding,
            'firstRegistrationDate': date_helper.get_isoformat(first_registration_dt),
            'lastServiceDate': date_helper.get_isoformat(last_service_date),
            'batteryExpiryDate': date_helper.get_isoformat(battery_expiry_date),
            'withdrawnReason': withdrawn_reason,
            'isArchived': is_archived,
            'createUserId': create_user_id,
            'createDate': date_helper.get_isoformat(create_dt),
            'updateUserId': update_user_id,
            'updateDate': date_helper.get_isoformat(update_dt),
            'versioning': versioning,
            'emergencyContact': {
                'details': emergency_contact
            },
            'note': note,
            'uses': [uses],
            'manufacturer': _get_beacon_manufacturer(fk_manufacturer_id),
            'beaconType': _get_beacon_type(fk_beacon_type_code),
            'model': _get_beacon_model(fk_model_code),
            'protocol': _get_beacon_protocol(fk_protocol_type_id)
        })

    return results

def _get_beacon_rows():
    cursor.execute(GET_ALL_BEACONS_QUERY)
    return cursor.fetchmany(5)
    # TODO: Get all beacons
    # return cursor.fetchall()

def _get_beacon_manufacturer(manufacturer_id):
    if (manufacturer_id == None):
        return manufacturer_id
    else:
        query = cursor.execute(f"""
        SELECT DESCRIPTION
        FROM TREF_BEACON_MANUFACTURERS
        WHERE PK_ID='{manufacturer_id}'
        """)
        
        manufacturer_row = query.fetchone()

        return manufacturer_row[0]

def _get_beacon_type(beacon_type_id):
    if (beacon_type_id == None):
        return beacon_type_id
    else:
        query = cursor.execute(f"""
        SELECT DESCRIPTION
        FROM TREF_BEACON_TYPES
        WHERE PK_CODE='{beacon_type_id}'
        """)
        
        beacon_type_row = query.fetchone()

        return beacon_type_row[0]

def _get_beacon_model(model_id):
    if (model_id == None):
        return model_id
    else:
        query = cursor.execute(f"""
        SELECT DESCRIPTION
        FROM TREF_BEACON_MODELS
        WHERE PK_CODE='{model_id}'
        """)
    
        model_row = query.fetchone()

        return model_row[0]

def _get_beacon_protocol(protocol_id):
    if (protocol_id == None):
        return protocol_id
    else:
        query = cursor.execute(f"""
        SELECT DESCRIPTION
        FROM TREF_BEACON_PROTOCOLS
        WHERE PK_ID='{protocol_id}'
        """)
    
        protocol_row = query.fetchone()

        return protocol_row[0]
