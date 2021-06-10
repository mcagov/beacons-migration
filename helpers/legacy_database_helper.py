import os
import cx_Oracle
import re
import csv

cx_Oracle.init_oracle_client(
    lib_dir=os.environ.get("HOME")+"/instantclient_19_8")


def get_db_connection():
    conn = cx_Oracle.connect(
        user="system",
        password="oracle",
        dsn="ec2-18-132-41-196.eu-west-2.compute.amazonaws.com/XE")
    # Set to desired Oracle schema
    conn.current_schema = 'CERSSVD_SCHEMA'
    print("Successfully connected to Oracle Database")
    return conn
