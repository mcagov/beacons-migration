import os
import sys
sys.path.append("./helpers")


import config_helper  # noqa
import legacy_database_helper  # noqa

directory = os.fsencode("./sql/cleansing")


def _runRules():
    conn = legacy_database_helper.get_db_connection()
    cursor = conn.cursor()
    print("Running through files in directory: ", directory)
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            file = open(os.path.abspath(os.path.join(dirpath, f)))
            sql_text = file.read()
            sql_commands = sql_text.split(";")
            for sql_command in sql_commands:
                if sql_command:
                    print(sql_command)
                    cursor.execute(sql_command)
                    cursor.fetchall()
                    print("Affected rows: ", cursor.rowcount)

    conn.commit()
    cursor.close()
    conn.close()


_runRules()
