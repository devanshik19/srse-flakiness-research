import datetime
import math
import pytest
from django.contrib.auth.models import User
from django.db.backends.sqlite3.base import _sqlite_datetime_extract

def test_sqlite_datetime_extract_week_day():
    dt = datetime.datetime(2023, 3, 14)  # Tuesday
    assert _sqlite_datetime_extract('week_day', dt) == 3

def test_sqlite_datetime_extract_week():
    dt = datetime.datetime(2023, 3, 14)  # 11th week of the year
    assert _sqlite_datetime_extract('week', dt) == 11

def test_sqlite_datetime_extract_quarter():
    dt = datetime.datetime(2023, 3, 14)  # Q1
    assert _sqlite_datetime_extract('quarter', dt) == 1

def test_sqlite_datetime_extract_iso_year():
    dt = datetime.datetime(2023, 3, 14)
    assert _sqlite_datetime_extract('iso_year', dt) == 2023

def test_sqlite_datetime_extract_none_for_invalid_lookup_type():
    dt = datetime.datetime(2023, 3, 14)
    assert _sqlite_datetime_extract('invalid', dt) is None

def test_sqlite_datetime_extract_none_for_none_datetime():
    assert _sqlite_datetime_extract('week_day', None) is None

def test_sqlite_datetime_extract_week_day_edge_case():
    dt = datetime.datetime(2023, 1, 1)  # Sunday
    assert _sqlite_datetime_extract('week_day', dt) == 1

def test_sqlite_datetime_extract_week_end_of_year():
    dt = datetime.datetime(2023, 12, 31)  # Last day of the year
    assert _sqlite_datetime_extract('week', dt) == 53  # 2023 ends with week 53