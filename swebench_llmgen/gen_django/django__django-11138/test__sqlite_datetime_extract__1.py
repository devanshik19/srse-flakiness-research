import pytest
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.backends.sqlite3.base import _sqlite_datetime_extract

def test_sqlite_datetime_extract():
    # Prepare test datetime values
    dt_utc = timezone.now()  # Current datetime in UTC
    dt_naive = dt_utc.replace(tzinfo=None)  # Naive datetime without timezone
    
    # Week day test
    assert _sqlite_datetime_extract('week_day', dt_utc) == (dt_utc.isoweekday() % 7) + 1
    assert _sqlite_datetime_extract('week_day', dt_naive) == (dt_naive.isoweekday() % 7) + 1
    
    # Week test
    assert _sqlite_datetime_extract('week', dt_utc) == dt_utc.isocalendar()[1]
    assert _sqlite_datetime_extract('week', dt_naive) == dt_naive.isocalendar()[1]
    
    # Quarter test
    assert _sqlite_datetime_extract('quarter', dt_utc) == (dt_utc.month - 1) // 3 + 1
    assert _sqlite_datetime_extract('quarter', dt_naive) == (dt_naive.month - 1) // 3 + 1
    
    # ISO year test
    assert _sqlite_datetime_extract('iso_year', dt_utc) == dt_utc.isocalendar()[0]
    assert _sqlite_datetime_extract('iso_year', dt_naive) == dt_naive.isocalendar()[0]
    
    # Testing unsupported lookup types
    assert _sqlite_datetime_extract('year', dt_utc) == dt_utc.year
    assert _sqlite_datetime_extract('month', dt_utc) == dt_utc.month
    assert _sqlite_datetime_extract('day', dt_utc) == dt_utc.day

    # Testing with None value
    assert _sqlite_datetime_extract('week_day', None) is None
    assert _sqlite_datetime_extract('week', None) is None
    assert _sqlite_datetime_extract('quarter', None) is None
    assert _sqlite_datetime_extract('iso_year', None) is None