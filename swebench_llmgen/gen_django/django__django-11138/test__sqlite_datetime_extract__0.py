import datetime
import pytest
from django.utils import timezone

from django.db.backends.sqlite3.base import _sqlite_datetime_extract

def test_sqlite_datetime_extract_week_day():
    dt = timezone.datetime(2023, 3, 15)  # Wednesday
    result = _sqlite_datetime_extract('week_day', dt)
    assert result == 4  # Wednesday is the 4th day of the week (ISO)

def test_sqlite_datetime_extract_week():
    dt = timezone.datetime(2023, 3, 15)  # Middle of March
    result = _sqlite_datetime_extract('week', dt)
    assert result == 11  # 2023-03-15 is in the 11th week of the year

def test_sqlite_datetime_extract_quarter():
    dt = timezone.datetime(2023, 3, 15)  # March is in Q1
    result = _sqlite_datetime_extract('quarter', dt)
    assert result == 1  # Q1

def test_sqlite_datetime_extract_iso_year():
    dt = timezone.datetime(2023, 3, 15)
    result = _sqlite_datetime_extract('iso_year', dt)
    assert result == 2023  # Should return the year

def test_sqlite_datetime_extract_invalid_lookup_type():
    dt = timezone.datetime(2023, 3, 15)
    result = _sqlite_datetime_extract('invalid_lookup', dt)
    assert result == dt.invalid_lookup  # Should gracefully raise an AttributeError

def test_sqlite_datetime_extract_none_datetime():
    result = _sqlite_datetime_extract('week', None)
    assert result is None  # Should return None if dt is None