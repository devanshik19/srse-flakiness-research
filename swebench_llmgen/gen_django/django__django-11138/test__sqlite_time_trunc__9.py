import pytest
import datetime
from django.db.backends import utils as backend_utils
from django.contrib.auth.models import User
from .base import _sqlite_time_trunc

def test_sqlite_time_trunc_hour():
    dt = datetime.datetime(2023, 10, 5, 14, 30, 45)
    result = _sqlite_time_trunc('hour', dt)
    assert result == "14:00:00"

def test_sqlite_time_trunc_minute():
    dt = datetime.datetime(2023, 10, 5, 14, 30, 45)
    result = _sqlite_time_trunc('minute', dt)
    assert result == "14:30:00"

def test_sqlite_time_trunc_second():
    dt = datetime.datetime(2023, 10, 5, 14, 30, 45)
    result = _sqlite_time_trunc('second', dt)
    assert result == "14:30:45"

def test_sqlite_time_trunc_none():
    result = _sqlite_time_trunc('hour', None)
    assert result is None

def test_sqlite_time_trunc_value_error():
    # Simulate a ValueError in typecasting
    class BadTime:
        pass

    result = _sqlite_time_trunc('hour', BadTime())
    assert result is None

def test_sqlite_time_trunc_type_error():
    # Simulate a TypeError in typecasting
    result = _sqlite_time_trunc('hour', "not a datetime")
    assert result is None