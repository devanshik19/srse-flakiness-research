import pytest
import datetime
from django.contrib.auth.models import User
from django.db.backends.sqlite3.base import _sqlite_datetime_extract

def test_sqlite_datetime_extract_week_day():
    dt = datetime.datetime(2023, 1, 1)  # A Sunday
    result = _sqlite_datetime_extract('week_day', dt)
    assert result == 1  # Sunday should return 1

def test_sqlite_datetime_extract_week():
    dt = datetime.datetime(2023, 1, 1)
    result = _sqlite_datetime_extract('week', dt)
    assert result == 52  # The week number for this date

def test_sqlite_datetime_extract_quarter():
    dt = datetime.datetime(2023, 4, 1)  # April is in Q2
    result = _sqlite_datetime_extract('quarter', dt)
    assert result == 2  # April belongs to the second quarter

def test_sqlite_datetime_extract_iso_year():
    dt = datetime.datetime(2023, 1, 1)
    result = _sqlite_datetime_extract('iso_year', dt)
    assert result == 2023  # ISO year should match the year

def test_sqlite_datetime_extract_none():
    result = _sqlite_datetime_extract('week', None)
    assert result is None  # Passing None should return None

def test_sqlite_datetime_extract_invalid_lookup_type():
    dt = datetime.datetime(2023, 1, 1)
    result = _sqlite_datetime_extract('invalid_type', dt)
    assert result == dt.invalid_type  # Should raise AttributeError