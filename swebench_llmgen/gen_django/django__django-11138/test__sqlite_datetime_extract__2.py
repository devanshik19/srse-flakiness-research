import datetime
import pytest
from django.contrib.auth.models import User
from django.db.backends.sqlite3.base import _sqlite_datetime_extract

def test_sqlite_datetime_extract():
    # Test valid datetime inputs with different lookup types
    dt_valid = datetime.datetime(2021, 3, 15, 12, 0, 0)
    
    # Test for week_day
    result = _sqlite_datetime_extract('week_day', dt_valid)
    assert result == 2  # Monday is 1, thus 15 March is 2

    # Test for week
    result = _sqlite_datetime_extract('week', dt_valid)
    assert result == 11  # 15 March 2021 is in the 11th week of the year

    # Test for quarter
    result = _sqlite_datetime_extract('quarter', dt_valid)
    assert result == 1  # March is in the first quarter

    # Test for iso_year
    result = _sqlite_datetime_extract('iso_year', dt_valid)
    assert result == 2021  # Year is 2021

    # Test for year
    result = _sqlite_datetime_extract('year', dt_valid)
    assert result == 2021  # Should return the same year

    # Test for month
    result = _sqlite_datetime_extract('month', dt_valid)
    assert result == 3  # March

    # Test for day
    result = _sqlite_datetime_extract('day', dt_valid)
    assert result == 15  # 15th day of the month

    # Test for hour
    result = _sqlite_datetime_extract('hour', dt_valid)
    assert result == 12  # 12 PM

    # Test for minute
    result = _sqlite_datetime_extract('minute', dt_valid)
    assert result == 0  # 0 minutes

    # Test for second
    result = _sqlite_datetime_extract('second', dt_valid)
    assert result == 0  # 0 seconds

    # Test for invalid lookup_type
    result = _sqlite_datetime_extract('invalid_type', dt_valid)
    assert result is None  # Should return None for invalid type

    # Test invalid datetime
    result = _sqlite_datetime_extract('week', None)
    assert result is None  # Should return None for None input

    result = _sqlite_datetime_extract('week', 'invalid_date')
    assert result is None  # Should return None for invalid string date