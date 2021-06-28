# Beacons Extract Transform & Load (ETL) Pipeline

## MAC setup

Ensure python 3.5+ is installed

Dependencies for the project are managed through [pipenv](https://pipenv.pypa.io/en/latest/#install-pipenv-today). To install `pipenv` run:
- `python3 -m pip install pipenv`

## Installing Dependencies

To install the dependencies for the project run:
- `pipenv install`

The Oracle [instantclient](https://www.oracle.com/database/technologies/instant-client/downloads.html) is required to connect to the Oracle instance.

To download the instantclient go to:

- [Download macOS instantclient](https://download.oracle.com/otn_software/mac/instantclient/198000/instantclient-basic-macos.x64-19.8.0.0.0dbru.zip)
- Unzip to directory `./instantclient_19_8`
- Run `pipenv run python push_single_owner_to_api.py`

**NOTE: When you run this for the first time macOS cannot verify the client files. You will have to open up: System Preferences > Security & Privacy and allow access to the files that cx_Oracle requires**

## IDE setup

If using PyCharm for your IDE setup, see the [docs for configuring pipenv](https://www.jetbrains.com/help/pycharm/pipenv.html#pipenv-existing-project).

## Running a script

cd to script in terminal
run python3 scriptnamehere.py
