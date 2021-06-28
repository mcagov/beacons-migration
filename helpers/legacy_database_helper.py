import logging
import os
import sys

import cx_Oracle

try:
    if sys.platform.startswith("darwin"):
        logging.info("Configuring instantclient for MacOS")
        lib_dir = os.path.join(os.getcwd(), "instantclient_19_8")
        cx_Oracle.init_oracle_client(lib_dir=lib_dir)
    elif sys.platform.startswith("linux"):
        logging.info("Configuring instantclient for Linux distribution")
        lib_dir = os.path.join(os.environ.get("ORACLE_HOME"), "instantclient_19_11")
        cx_Oracle.init_oracle_client(lib_dir=lib_dir)
except Exception as err:
    logging.info("Unable to instantiate Oracle instantclient")
    logging.error(err)
    sys.exit(1)


def get_db_connection():
    conn = cx_Oracle.connect(
        user="system",
        password="oracle",
        dsn="ec2-18-132-41-196.eu-west-2.compute.amazonaws.com/XE")
    # Set to desired Oracle schema
    conn.current_schema = 'CERSSVD_SCHEMA'
    logging.info("Successfully connected to Oracle Database")
    return conn
