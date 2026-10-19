import pytest
import datetime
from django.db.backends.sqlite3.base import _sqlite_datetime_extract

def test_sqlite_datetime_extract():
    # Test cases for each lookup_type in _sqlite_datetime_extract
    
    # Test for 'week_day'
    dt = datetime.datetime(2022, 1, 1)  # Saturday
    assert _sqlite_datetime_extract('week_day', dt) == 7  # Isoweekday() is 6, so % 7 + 1 = 7

    # Test for 'week'
    dt = datetime.datetime(2022, 1, 1)  # First week of the year
    assert _sqlite_datetime_extract('week', dt) == 52  # January 1, 2022 is in the ISO week 52 of 2021

    # Test for 'quarter'
    dt = datetime.datetime(2022, 1, 1)  # First quarter
    assert _sqlite_datetime_extract('quarter', dt) == 1

    # Test for 'iso_year'
    dt = datetime.datetime(2022, 1, 1)
    assert _sqlite_datetime_extract('iso_year', dt) == 2022

    # Test for 'year'
    dt = datetime.datetime(2022, 1, 1)
    assert _sqlite_datetime_extract('year', dt) == 2022

    # Test for 'month'
    dt = datetime.datetime(2022, 1, 1)
    assert _sqlite_datetime_extract('month', dt) == 1

    # Test for 'day'
    dt = datetime.datetime(2022, 1, 1)
    assert _sqlite_datetime_extract('day', dt) == 1

    # Test for 'hour'
    dt = datetime.datetime(2022, 1, 1, 12)
    assert _sqlite_datetime_extract('hour', dt) == 12

    # Test for 'minute'
    dt = datetime.datetime(2022, 1, 1, 12, 30)
    assert _sqlite_datetime_extract('minute', dt) == 30

    # Test for 'second'
    dt = datetime.datetime(2022, 1, 1, 12, 30, 45)
    assert _sqlite_datetime_extract('second', dt) == 45

    # Test with None datetime input
    assert _sqlite_datetime_extract('week_day', None) is None
    assert _sqlite_datetime_extract('week', None) is None