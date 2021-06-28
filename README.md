# Beacons Extract Transform & Load (ETL) Pipeline

## MAC setup

Ensure python 3.5+ is installed

Dependencies for the project are managed through [pipenv](https://pipenv.pypa.io/en/latest/#install-pipenv-today). To install `pipenv` run:
- `python3 -m pip install pipenv`

## Installing Dependencies

To install the dependencies for the project run:
- `pipenv install`

The Oracle [instantclient](https://www.oracle.com/database/technologies/instant-client/downloads.html) is required to connect to the Oracle DB.

This is configured for 

## IDE setup

If using PyCharm for your IDE setup, see the [docs for configuring pipenv](https://www.jetbrains.com/help/pycharm/pipenv.html#pipenv-existing-project).

Install cx_Oracle (Enables connections to oracle instances):
https://cx-oracle.readthedocs.io/en/latest/user_guide/installation.html

## Running a script

cd to script in terminal
run python3 scriptnamehere.py
