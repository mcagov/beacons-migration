import os
import csv

from helpers.legacy_database_helper import get_db_connection

"""
Find all owners with >1 beacon aggregated by owner email.
For each of those emails, attempt aggregation and output CSV of all variants when safe aggregation fails.
Record all email addresses where safe aggregation succeeds.
"""


def find_bulk_beacon_owners(bulk_beacon_number):
    os.makedirs("bulk_csv", exist_ok=True)
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            query = cursor.execute("""
                SELECT  LOWER(EMAIL), COUNT(LOWER(EMAIL)) AS COUNT
                FROM BEACON_OWNERS_CLEANED
                JOIN BEACONS b on b.PK_BEACON_ID = FK_BEACON_ID
                WHERE IS_MAIN = 'Y' AND OWNER_NAME != 'DELETED' AND b.IS_ARCHIVED = 'N' AND b.IS_WITHDRAWN = 'N'
                GROUP BY LOWER(EMAIL)
                HAVING COUNT(LOWER(EMAIL)) > 1
                ORDER BY COUNT(LOWER(EMAIL)) DESC
                """)
            # Dummy loop here, using query.fetchmany() each time to return a bunch of rows.
            total_all = 0
            total_fail_agg = 0
            total_safe_agg = 0
            total_manual_agg = 0
            fail_agg_csvfile = open('safe_aggregates.csv', 'w', newline='')
            fail_agg_csvwriter = csv.writer(fail_agg_csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            fail_agg_csvwriter.writerow(['total', 'email'])
            safe_agg_csvfile = open('safe_aggregates.csv', 'w', newline='')
            safe_agg_csvwriter = csv.writer(safe_agg_csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            safe_agg_csvwriter.writerow(['total', 'email'])
            while True:
                rows = query.fetchmany()
                if rows == []:
                    # No more results
                    break

                for email, total in rows:
                    total_all = total_all + total
                    # For each row query number of 'versions' of the owner if we were to perform safe aggregation
                    owner_sql = """
                    SELECT COUNT(EMAIL) AS COUNT, UPPER(EMAIL), UPPER(OWNER_NAME), UPPER(COMPANY_NAME), UPPER(CARE_OF), UPPER(PHONE_1), UPPER(PHONE_2),
                    UPPER(MOBILE_1), UPPER(MOBILE_2), UPPER(POST_CODE), UPPER(ADDRESS_1), UPPER(ADDRESS_2), UPPER(ADDRESS_3),
                    UPPER(ADDRESS_4), UPPER(COUNTRY)
                    FROM BEACON_OWNERS_CLEANED
                    JOIN BEACONS b on b.PK_BEACON_ID = FK_BEACON_ID
                    WHERE IS_MAIN = 'Y' AND OWNER_NAME != 'DELETED' AND b.IS_ARCHIVED = 'N' AND b.IS_WITHDRAWN = 'N'
                    AND EMAIL like :email
                    GROUP BY UPPER(EMAIL), UPPER(OWNER_NAME), UPPER(COMPANY_NAME), UPPER(CARE_OF), UPPER(PHONE_1), UPPER(PHONE_2),
                        UPPER(MOBILE_1), UPPER(MOBILE_2), UPPER(POST_CODE), UPPER(ADDRESS_1), UPPER(ADDRESS_2), UPPER(ADDRESS_3),
                        UPPER(ADDRESS_4), UPPER(COUNTRY)
                    ORDER BY UPPER(EMAIL), UPPER(EMAIL), UPPER(OWNER_NAME), UPPER(COMPANY_NAME), UPPER(CARE_OF), UPPER(PHONE_1), UPPER(PHONE_2),
                        UPPER(MOBILE_1), UPPER(MOBILE_2), UPPER(POST_CODE), UPPER(ADDRESS_1), UPPER(ADDRESS_2), UPPER(ADDRESS_3),
                        UPPER(ADDRESS_4), UPPER(COUNTRY) DESC
                    """
                    owner_cursor = conn.cursor()
                    owner_cursor.execute(owner_sql, [email])
                    owner_rows = owner_cursor.fetchall()

                    if total > bulk_beacon_number and len(owner_rows) > 1:
                        # email associated with bulk number of beacons fails to aggregate safely. Output variants.
                        total_manual_agg = total_manual_agg + total
                        filename = str(len(owner_rows)) + '_' + str(total) + '_' + email + '.csv'
                        with open(filename, 'w', newline='') as csvfile:
                            csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                            csvwriter.writerow(
                                ['total', 'email', 'owner_name', 'company_name', 'care_of', 'phone_1', 'phone_2',
                                 'mobile_1',
                                 'mobile_2', 'post_code', 'address_1', 'address_2', 'address_3', 'address_4',
                                 'country'])
                            for r in owner_rows:
                                # output to CSV
                                csvwriter.writerow(r)
                        os.rename(filename, 'bulk_csv/' + filename)
                    elif len(owner_rows) == 1:
                        # These will get safely aggregated
                        total_safe_agg = total_safe_agg + total
                        safe_agg_csvwriter.writerow([total, email])
                    else:
                        # email fails to aggregate safely and associated with <= bulk number. These will fail to aggregate on migration.
                        total_fail_agg = total_fail_agg + total
                        fail_agg_csvwriter.writerow([total, email])

            print(f'Total beacons: {str(total_all)}')
            print("Manual cleanup required: " + str(total_manual_agg) + "(" + str(
                round((total_manual_agg / total_all) * 100)) + "%)")
            print("Safe aggregation: " + str(total_safe_agg) + "(" + str(
                round((total_safe_agg / total_all) * 100)) + "%)")
            print("Fail aggregation: " + str(total_fail_agg) + "(" + str(
                round((total_fail_agg / total_all) * 100)) + "%)")


if __name__ == '__main__':
    bulk_number = 30
    print(f'Aggregating owners with more than {bulk_number} beacons')
    find_bulk_beacon_owners(bulk_number)
