from datetime import datetime, timedelta
from src.helpers.date_helper import earliest_date, latest_date, get_isoformat


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


def test_returns_None_if_argument_is_None():
    assert get_isoformat(None) is None


def test_returns_argument_if_it_is_not_a_datetime():
    not_a_date = "I am not a date"
    assert get_isoformat(not_a_date) == not_a_date


def test_returns_argument_if_it_is_not_a_datetime():
    date = datetime.now()
    date_as_iso_string = date.isoformat()

    assert get_isoformat(date) == date_as_iso_string
