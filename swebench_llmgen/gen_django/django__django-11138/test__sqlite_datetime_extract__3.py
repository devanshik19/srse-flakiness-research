import datetime
import math
import pytest
from django.contrib.auth.models import User
from django.db.backends.sqlite3.base import _sqlite_datetime_extract

def test_sqlite_datetime_extract():
    # Create a user instance to ensure we have a valid setup
    User.objects.create(username='testuser')

    # Test cases for each branch
    # 1. week_day
    dt1 = datetime.datetime(2023, 3, 25, 10, 0, 0)
    result1 = _sqlite_datetime_extract('week_day', dt1)
    assert result1 == 6  # Saturday -> 6

    # 2. week
    result2 = _sqlite_datetime_extract('week', dt1)
    assert result2 == 12  # 2023-03-25 is in the 12th week of the year

    # 3. quarter
    result3 = _sqlite_datetime_extract('quarter', dt1)
    assert result3 == 1  # March is in the first quarter

    # 4. iso_year
    result4 = _sqlite_datetime_extract('iso_year', dt1)
    assert result4 == 2023  # The year of the datetime

    # 5. Check for existence of other attributes
    dt2 = datetime.datetime(2023, 3, 25, 10, 0, 0)
    result5 = _sqlite_datetime_extract('year', dt2)
    assert result5 == 2023

    # 6. Invalid lookup type should just return the attribute if it exists.
    result6 = _sqlite_datetime_extract('microsecond', dt2)
    assert result6 == 0  # Should return the microsecond part of the datetime

    # 7. Invalid datetime (should return None)
    result7 = _sqlite_datetime_extract('week_day', None)
    assert result7 is None