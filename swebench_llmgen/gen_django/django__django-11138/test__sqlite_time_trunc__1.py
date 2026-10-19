import pytest
import datetime
from django.db.backends import utils as backend_utils
from django.contrib.auth.models import User

def test_sqlite_time_trunc_valid_cases():
    assert _sqlite_time_trunc('hour', datetime.time(12, 34, 56)) == "12:00:00"
    assert _sqlite_time_trunc('minute', datetime.time(12, 34, 56)) == "12:34:00"
    assert _sqlite_time_trunc('second', datetime.time(12, 34, 56)) == "12:34:56"

def test_sqlite_time_trunc_invalid_cases():
    assert _sqlite_time_trunc('hour', None) is None
    assert _sqlite_time_trunc('minute', "not a time") is None
    assert _sqlite_time_trunc('second', 123) is None

def test_sqlite_time_trunc_edge_cases():
    assert _sqlite_time_trunc('hour', datetime.time(0, 0, 0)) == "00:00:00"
    assert _sqlite_time_trunc('minute', datetime.time(0, 0, 0)) == "00:00:00"
    assert _sqlite_time_trunc('second', datetime.time(0, 0, 0)) == "00:00:00"