import datetime
import pytest
from django.db.backends import utils as backend_utils
from django.contrib.auth.models import User
from django.utils import timezone

# The focal function to be tested
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

# The test cases for _sqlite_time_trunc function
@pytest.mark.parametrize("lookup_type, dt, expected", [
    ('hour', datetime.time(12, 34, 56), "12:00:00"),
    ('minute', datetime.time(12, 34, 56), "12:34:00"),
    ('second', datetime.time(12, 34, 56), "12:34:56"),
    ('hour', datetime.time(0, 0, 0), "00:00:00"),
    ('minute', datetime.time(0, 0, 0), "00:00:00"),
    ('second', datetime.time(0, 0, 0), "00:00:00"),
    ('hour', None, None),
    ('minute', None, None),
    ('second', None, None),
])
def test_sqlite_time_trunc(lookup_type, dt, expected):
    assert _sqlite_time_trunc(lookup_type, dt) == expected

def test_sqlite_time_trunc_invalid_type():
    with pytest.raises(ValueError):
        _sqlite_time_trunc('hour', 'invalid_time')
        
    with pytest.raises(TypeError):
        _sqlite_time_trunc('minute', 12345)