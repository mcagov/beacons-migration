from datetime import datetime, timedelta

from src.aggregate_owners import earliest_date, latest_date


def test_returns_the_earliest_date():
    now = datetime.now()
    before = now - timedelta(1)
    assert earliest_date([now, before]) == before


def test_returns_the_earliest_date_for_the_same_dates():
    now = datetime.now()
    assert earliest_date([now, now]) == now


def test_returns_the_earliest_date_with_none_in_the_date_list():
    now = datetime.now()
    assert earliest_date([now, None]) == now


def test_handles_multiple_of_the_same_dates():
    now = datetime.now()
    before = now - timedelta(1)
    assert earliest_date([now, before, now, before]) == before


def test_returns_the_latest_date():
    now = datetime.now()
    before = now - timedelta(1)
    assert latest_date([now, before]) == now


def test_returns_the_latest_date_for_the_same_dates():
    now = datetime.now()
    assert latest_date([now, now]) == now


def test_returns_the_latest_date_with_none_in_the_date_list():
    now = datetime.now()
    assert latest_date([None, now]) == now


def test_returns_the_latest_date_for_multiple_dates():
    now = datetime.now()
    before = now - timedelta(1)
    assert latest_date([now, before, now, before]) == now
