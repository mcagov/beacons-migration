import src.helpers.legacy_database_helper as legacy_database_helper
import src.helpers.date_helper as date_helper

db_connection = legacy_database_helper.get_db_connection()
cursor = db_connection.cursor()

def get_uses(beacon_id):
    uses = _get_use_rows(beacon_id)

    results = []

    for pk_beacon_uses_id, fk_beacon_id, fk_use_type_code, vessel_name, home_port, \
        max_persons, official_number, rss_ssr_number, call_sign, imo_number, \
        mmsi_number, fishing_vessel_pln, fk_vessel_type_id, hull_id_number, \
        cg66_ref_number, fk_aircraft_type_id, aod_serial_number, principal_airport, \
        bit_24_address_hex, aircraft_registration_mark, fk_land_use_id, area_of_use, \
        trip_info, rig_name, beacon_position, position, fk_mod_type_code, \
        fk_activation_mode_code, fk_variant_code, local_management_id, beacon_nsn, \
        beacon_part_number, mod_status, note, pennant_number, aircraft_description, \
        survival_craft_type, communications, is_main, create_user_id, create_dt, \
        update_user_id, update_dt, versioning in uses:
    
        results.append({
            'pkBeaconUsesId': pk_beacon_uses_id,
            'fkBeaconId': fk_beacon_id,
            'vesselName': vessel_name,
            'homePort': home_port,
            'maxPersons': max_persons,
            'officialNumber': official_number,
            'rssSsrNumber': rss_ssr_number,
            'callSign': call_sign,
            'imoNumber': imo_number,
            'mmsiNumber': mmsi_number,
            'fishingVesselPln': fishing_vessel_pln,
            'hullIdNumber': hull_id_number,
            'cg66RefNumber': cg66_ref_number,
            'aodSerialNumber': aod_serial_number,
            'principalAirport': principal_airport,
            'bit24AddressHex': bit_24_address_hex,
            'aircraftRegistrationMark': aircraft_registration_mark,
            'areaOfUse': area_of_use,
            'tripInfo': trip_info,
            'rigName': rig_name,
            'beaconPosition': beacon_position,
            'position': position,
            'localManagementId': local_management_id,
            'beaconNsn': beacon_nsn,
            'beaconPartNumber': beacon_part_number,
            'modStatus': mod_status,
            'note': note,
            'pennantNumber': pennant_number,
            'aircraftDescription': aircraft_description,
            'survivalCraftType': survival_craft_type,
            'communications': communications,
            'isMain': is_main,
            'createUserId': create_user_id,
            'createDt': date_helper.get_isoformat(create_dt),
            'updateUserId': update_user_id,
            'updateDt': date_helper.get_isoformat(update_dt),
            'versioning': versioning,
            'useType': _get_use_type(fk_use_type_code),
            'vesselType': _get_vessel_type(fk_vessel_type_id),
            'aircraftType': _get_aircraft_type(fk_aircraft_type_id),
            'landUse': _get_land_use(fk_land_use_id)
        })

    return results

def _get_use_rows(beacon_id):
    query = cursor.execute(f"""
        SELECT * FROM BEACON_USES
        WHERE FK_BEACON_ID='{beacon_id}'
    """)

    return query.fetchall()

def _get_use_type(use_type_id):
    if (use_type_id == None):
        return use_type_id
    else:
        query = cursor.execute(f"""
        SELECT DESCRIPTION
        FROM TREF_BEACON_USE_TYPES
        WHERE PK_CODE='{use_type_id}'
        """)
        
        use_type_row = query.fetchone()

        return use_type_row[0]

def _get_vessel_type(vessel_type_id):
    if (vessel_type_id == None):
        return vessel_type_id
    else:
        query = cursor.execute(f"""
        SELECT DESCRIPTION
        FROM TREF_BEACON_VESSEL_TYPES
        WHERE PK_ID='{vessel_type_id}'
        """)
        
        vessel_type_row = query.fetchone()

        return vessel_type_row[0]

def _get_aircraft_type(aircraft_type_id):
    if (aircraft_type_id == None):
        return aircraft_type_id
    else:
        query = cursor.execute(f"""
        SELECT DESCRIPTION
        FROM TREF_BEACON_AIRCRAFT_TYPES
        WHERE PK_ID='{aircraft_type_id}'
        """)
        
        aircraft_type_row = query.fetchone()

        return aircraft_type_row[0]

def _get_land_use(land_use_id):
    if (land_use_id == None):
        return land_use_id
    else:
        query = cursor.execute(f"""
        SELECT DESCRIPTION
        FROM TREF_BEACON_LAND_USE
        WHERE PK_ID='{land_use_id}'
        """)
        
        land_use_row = query.fetchone()

        return land_use_row[0]
