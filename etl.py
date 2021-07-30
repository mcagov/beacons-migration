from datetime import datetime
from src.owner_cleansing_rules import run_owner_cleansing_rules
from src.push_beacons_to_api import push_beacons


def _now():
    return datetime.now()


def run_migration():
    print(f'Running ETL migration {_now()}')
    print(f'Running cleansing owner rules {_now()}')
    run_owner_cleansing_rules()
    push_beacons()


if __name__ == '__main__':
    run_migration()
