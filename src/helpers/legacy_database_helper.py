import os
import sys

import cx_Oracle
from src.helpers.config_helper import get_config_parser

try:
    if sys.platform.startswith("darwin"):
        print("Configuring instantclient for MacOS")
        lib_dir = os.path.join(os.getcwd(), "instantclient_19_8")
        cx_Oracle.init_oracle_client(lib_dir=lib_dir)
    elif sys.platform.startswith("linux"):
        print("Configuring instantclient for Linux distribution")
        lib_dir = os.path.join(os.environ.get("ORACLE_HOME"), "instantclient_19_11")
        cx_Oracle.init_oracle_client(lib_dir=lib_dir)
except Exception as err:
    print("Unable to instantiate Oracle instantclient")
    print(err)
    sys.exit(1)


def get_db_connection():
    oracle_uri = get_config_parser().get('oracle_uri')
    conn = cx_Oracle.connect(
        user="system",
        password="oracle",
        dsn=f'{oracle_uri}/XE')
    # Set to desired Oracle schema
    conn.current_schema = 'CERSSVD_SCHEMA'
    print("Successfully connected to Oracle Database")

    return conn
