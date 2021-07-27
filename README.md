# Beacons Extract Transform & Load (ETL) Pipeline

Please see the [Beacons Miro board](https://miro.com/app/board/o9J_lRB60BQ=/) for more information on the migration.

# Running the migration

There are three GitHub Actions pipelines setup to run the migration against the [Development](https://github.com/mcagov/beacons-etl/actions/workflows/dev-migration.yml), [Staging](https://github.com/mcagov/beacons-etl/actions/workflows/staging-migration.yml), and [Production](https://github.com/mcagov/beacons-etl/actions/workflows/production-migration.yml) environments.

Each pipeline will standup the latest backups for the Oracle DB and run the migration against each environment. TODO: there will be a report(s) uploaded to GitHub where you can inspect the result of the migration run.

See the GitHub Actions yaml files for more information.

## Running the migration locally

Ensure that you have the Oracle DB containing the existing records, and the Beacons API stood up locally.

Then, from the root of the project run the following:

> pipenv run python _script_to_run_.py

## MAC setup

Ensure python 3.5+ is installed

Dependencies for the project are managed through [pipenv](https://pipenv.pypa.io/en/latest/#install-pipenv-today). To install `pipenv` run:

- `python3 -m pip install pipenv`

## Connecting to the Oracle DB

The Oracle DB connection string is set in the [legacy database helper file](src/helpers/legacy_database_helper.py). To standup a local Oracle DB instance
see the docs in the [Beacons Oracle GitHub repo](https://github.com/mcagov/beacons-oracle#restoring-the-latest-backups-locally).

## Installing Dependencies

To install the dependencies for the project run:

- `pipenv install --dev`

The Oracle [instantclient](https://www.oracle.com/database/technologies/instant-client/downloads.html) is required to connect to the Oracle instance.

To download the instantclient go to:

- [Download macOS instantclient](https://download.oracle.com/otn_software/mac/instantclient/198000/instantclient-basic-macos.x64-19.8.0.0.0dbru.zip)
- Unzip to directory `./instantclient_19_8` in this repository's directory
- Run `pipenv run python run_cleansing_rules.py`

**NOTE: When you run this for the first time macOS cannot verify the client files. You will have to open up: System Preferences > Security & Privacy and allow access to the files that cx_Oracle requires**

## Running Unit Tests

[PyTest](https://docs.pytest.org/en/6.2.x/contents.html) is used for unit testing. To run all the unit tests run:

> pipenv run pytest

## IDE setup

If using PyCharm for your IDE setup, see the [docs for configuring pipenv](https://www.jetbrains.com/help/pycharm/pipenv.html#pipenv-existing-project).
