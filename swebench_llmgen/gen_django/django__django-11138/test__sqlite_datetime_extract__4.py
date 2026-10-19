import datetime
import pytest
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.backends.sqlite3.base import _sqlite_datetime_extract

def test_sqlite_datetime_extract_week_day():
    dt = timezone.make_aware(datetime.datetime(2021, 1, 1))  # Friday
    assert _sqlite_datetime_extract('week_day', dt) == 5

def test_sqlite_datetime_extract_week():
    dt = timezone.make_aware(datetime.datetime(2021, 1, 1))
    assert _sqlite_datetime_extract('week', dt) == 53  # ISO week number

def test_sqlite_datetime_extract_quarter():
    dt = timezone.make_aware(datetime.datetime(2021, 1, 1))
    assert _sqlite_datetime_extract('quarter', dt) == 1

def test_sqlite_datetime_extract_iso_year():
    dt = timezone.make_aware(datetime.datetime(2021, 1, 1))
    assert _sqlite_datetime_extract('iso_year', dt) == 2021

def test_sqlite_datetime_extract_invalid_lookup_type():
    dt = timezone.make_aware(datetime.datetime(2021, 1, 1))
    assert _sqlite_datetime_extract('non_existing_field', dt) == 1  # should return a default value

def test_sqlite_datetime_extract_invalid_datetime():
    assert _sqlite_datetime_extract('week_day', None) is None
    assert _sqlite_datetime_extract('week', None) is None