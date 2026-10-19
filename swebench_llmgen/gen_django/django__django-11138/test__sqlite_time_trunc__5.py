import pytest
import datetime
from django.db.backends import utils as backend_utils
from django.contrib.auth.models import User
from your_module_path import _sqlite_time_trunc  # Adjust this import based on your module path

def test_sqlite_time_trunc_hour():
    dt = datetime.time(10, 20, 30)
    result = _sqlite_time_trunc('hour', dt)
    assert result == "10:00:00"

def test_sqlite_time_trunc_minute():
    dt = datetime.time(10, 20, 30)
    result = _sqlite_time_trunc('minute', dt)
    assert result == "10:20:00"

def test_sqlite_time_trunc_second():
    dt = datetime.time(10, 20, 30)
    result = _sqlite_time_trunc('second', dt)
    assert result == "10:20:30"

def test_sqlite_time_trunc_none():
    result = _sqlite_time_trunc('hour', None)
    assert result is None

def test_sqlite_time_trunc_invalid_type():
    class InvalidTime:
        pass
    
    dt = InvalidTime()
    result = _sqlite_time_trunc('hour', dt)
    assert result is None

def test_sqlite_time_trunc_invalid_lookup_type():
    dt = datetime.time(10, 20, 30)
    result = _sqlite_time_trunc('invalid', dt)
    assert result is None