import pytest
from django.utils import timezone
from django.db.backends import utils as backend_utils
from django.contrib.auth.models import User
from django.db import models

# Assuming the focal function _sqlite_time_trunc is imported from the module
from django.db.backends.sqlite3.base import _sqlite_time_trunc 

def test_sqlite_time_trunc_hour():
    dt = timezone.datetime(2023, 1, 1, 10, 15, 45)
    assert _sqlite_time_trunc('hour', dt) == "10:00:00"

def test_sqlite_time_trunc_minute():
    dt = timezone.datetime(2023, 1, 1, 10, 15, 45)
    assert _sqlite_time_trunc('minute', dt) == "10:15:00"

def test_sqlite_time_trunc_second():
    dt = timezone.datetime(2023, 1, 1, 10, 15, 45)
    assert _sqlite_time_trunc('second', dt) == "10:15:45"

def test_sqlite_time_trunc_none():
    assert _sqlite_time_trunc('hour', None) is None
    assert _sqlite_time_trunc('minute', None) is None
    assert _sqlite_time_trunc('second', None) is None

def test_sqlite_time_trunc_invalid_type():
    with pytest.raises((ValueError, TypeError)):
        _sqlite_time_trunc('hour', "invalid datetime")