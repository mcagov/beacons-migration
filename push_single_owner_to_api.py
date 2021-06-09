import cx_Oracle

def _getDBConnection():
    conn = cx_Oracle.connect(
        user="system",
        password="oracle",
        dsn="localhost/XE")
    # Set to desired Oracle schema
    conn.current_schema = 'CERSSVD_SCHEMA'
    print("Successfully connected to Oracle Database")
    return conn

connection = _getDBConnection()
    cursor = connection.cursor()
    cursor.execute("""
        begin
            execute immediate 'drop table BEACON_OWNERS_CLEANED';
            exception when others then if sqlcode <> -942 then raise; end if;
        end;""")
    cursor.execute("""CREATE TABLE BEACON_OWNERS_CLEANED AS SELECT * FROM BEACON_OWNERS WHERE 1=0""")
    cursor.close()
    connection.close()