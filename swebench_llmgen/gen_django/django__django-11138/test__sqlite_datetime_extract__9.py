import datetime
import math
import pytest
from django.contrib.auth.models import User
from django.db.backends.sqlite3.base import _sqlite_datetime_extract

def test_sqlite_datetime_extract():
    # Test cases for different lookup types
    tzname = 'UTC'
    
    # Week day test (1-7)
    dt1 = datetime.datetime(2021, 10, 5, tzinfo=datetime.timezone.utc)  # Tuesday
    assert _sqlite_datetime_extract('week_day', dt1, tzname) == 3  # Should return 3

    # Week test
    dt2 = datetime.datetime(2021, 1, 1, tzinfo=datetime.timezone.utc)  # New Year's Day
    assert _sqlite_datetime_extract('week', dt2, tzname) == 53  # Should return ISO week number

    # Quarter test
    dt3 = datetime.datetime(2021, 5, 1, tzinfo=datetime.timezone.utc)  # May (Q2)
    assert _sqlite_datetime_extract('quarter', dt3, tzname) == 2  # Should return quarter 2

    # ISO year test
    dt4 = datetime.datetime(2020, 12, 31, tzinfo=datetime.timezone.utc)  # Last day of 2020
    assert _sqlite_datetime_extract('iso_year', dt4, tzname) == 2020  # Should return 2020

    # Additional attribute test (returning year, as an example)
    assert _sqlite_datetime_extract('year', dt4, tzname) == 2020  # Should return 2020

    # Invalid lookup type should return the attribute error
    with pytest.raises(AttributeError):
        _sqlite_datetime_extract('invalid_lookup', dt4, tzname)

    # None case
    assert _sqlite_datetime_extract('week_day', None, tzname) is None  # Should return None