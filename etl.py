from datetime import datetime

from src.owner_cleansing_rules import run_owner_cleansing_rules


def _now():
    return datetime.now()


def run_migration():
    print(f'Running ETL migration {_now()}')
    print(f'Running cleansing owner rules {_now()}')
    run_owner_cleansing_rules()


if __name__ == '__main__':
    run_migration()
