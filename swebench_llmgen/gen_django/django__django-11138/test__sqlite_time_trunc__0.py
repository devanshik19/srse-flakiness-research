import datetime
import pytest
from django.db.backends import utils as backend_utils
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.backends.sqlite3.base import _sqlite_time_trunc

def test_sqlite_time_trunc_none():
    assert _sqlite_time_trunc('hour', None) is None
    assert _sqlite_time_trunc('minute', None) is None
    assert _sqlite_time_trunc('second', None) is None

def test_sqlite_time_trunc_invalid_type():
    assert _sqlite_time_trunc('hour', 'invalid') is None
    assert _sqlite_time_trunc('minute', 'invalid') is None
    assert _sqlite_time_trunc('second', 'invalid') is None

def test_sqlite_time_trunc_hour():
    dt = timezone.datetime(2023, 3, 15, 12, 30, 45)
    assert _sqlite_time_trunc('hour', dt) == "12:00:00"

def test_sqlite_time_trunc_minute():
    dt = timezone.datetime(2023, 3, 15, 12, 30, 45)
    assert _sqlite_time_trunc('minute', dt) == "12:30:00"

def test_sqlite_time_trunc_second():
    dt = timezone.datetime(2023, 3, 15, 12, 30, 45)
    assert _sqlite_time_trunc('second', dt) == "12:30:45"