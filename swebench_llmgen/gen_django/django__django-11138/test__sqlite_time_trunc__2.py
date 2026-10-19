import pytest
import datetime
from django.db.backends import utils as backend_utils
from django.utils import timezone

from django.contrib.auth.models import User

def _sqlite_time_trunc(lookup_type, dt):
    if dt is None:
        return None
    try:
        dt = backend_utils.typecast_time(dt)
    except (ValueError, TypeError):
        return None
    if lookup_type == 'hour':
        return "%02i:00:00" % dt.hour
    elif lookup_type == 'minute':
        return "%02i:%02i:00" % (dt.hour, dt.minute)
    elif lookup_type == 'second':
        return "%02i:%02i:%02i" % (dt.hour, dt.minute, dt.second)

def test_sqlite_time_trunc_hours():
    dt = timezone.datetime(2023, 10, 1, 14, 30, 45)
    assert _sqlite_time_trunc('hour', dt) == "14:00:00"

def test_sqlite_time_trunc_minutes():
    dt = timezone.datetime(2023, 10, 1, 14, 30, 45)
    assert _sqlite_time_trunc('minute', dt) == "14:30:00"

def test_sqlite_time_trunc_seconds():
    dt = timezone.datetime(2023, 10, 1, 14, 30, 45)
    assert _sqlite_time_trunc('second', dt) == "14:30:45"

def test_sqlite_time_trunc_none():
    assert _sqlite_time_trunc('hour', None) is None

def test_sqlite_time_trunc_invalid_lookup():
    dt = timezone.datetime(2023, 10, 1, 14, 30, 45)
    assert _sqlite_time_trunc('invalid', dt) is None

def test_sqlite_time_trunc_invalid_datetime():
    invalid_dt = "not_a_datetime"
    assert _sqlite_time_trunc('hour', invalid_dt) is None