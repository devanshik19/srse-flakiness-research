import pytest
import datetime
import math
from django.contrib.auth.models import User
from django.db.backends.sqlite3.base import _sqlite_datetime_extract

def test_sqlite_datetime_extract_week_day():
    dt = datetime.datetime(2023, 1, 15)  # Sunday
    assert _sqlite_datetime_extract('week_day', dt) == 7
    dt = datetime.datetime(2023, 1, 16)  # Monday
    assert _sqlite_datetime_extract('week_day', dt) == 1

def test_sqlite_datetime_extract_week():
    dt = datetime.datetime(2023, 1, 1)
    assert _sqlite_datetime_extract('week', dt) == 52  # ISO week number

def test_sqlite_datetime_extract_quarter():
    dt = datetime.datetime(2023, 1, 1)
    assert _sqlite_datetime_extract('quarter', dt) == 1
    dt = datetime.datetime(2023, 7, 1)
    assert _sqlite_datetime_extract('quarter', dt) == 3

def test_sqlite_datetime_extract_iso_year():
    dt = datetime.datetime(2023, 1, 1)
    assert _sqlite_datetime_extract('iso_year', dt) == 2023

def test_sqlite_datetime_extract_invalid_lookup_type():
    dt = datetime.datetime(2023, 1, 1)
    assert _sqlite_datetime_extract('invalid_lookup_type', dt) is None

def test_sqlite_datetime_extract_none_datetime():
    assert _sqlite_datetime_extract('week', None) is None
    assert _sqlite_datetime_extract('quarter', None) is None
    assert _sqlite_datetime_extract('iso_year', None) is None