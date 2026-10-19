import pytest
import datetime
from django.db.backends import utils as backend_utils
from django.db.backends.sqlite3.base import _sqlite_time_trunc

def test_sqlite_time_trunc():
    # Test for None input
    assert _sqlite_time_trunc('hour', None) is None
    assert _sqlite_time_trunc('minute', None) is None
    assert _sqlite_time_trunc('second', None) is None

    # Test valid datetime input
    dt = backend_utils.typecast_time(datetime.time(12, 34, 56))
    
    assert _sqlite_time_trunc('hour', dt) == "12:00:00"
    assert _sqlite_time_trunc('minute', dt) == "12:34:00"
    assert _sqlite_time_trunc('second', dt) == "12:34:56"

    # Test invalid datetime input
    assert _sqlite_time_trunc('hour', "not a datetime") is None
    assert _sqlite_time_trunc('minute', "invalid data") is None
    assert _sqlite_time_trunc('second', 123) is None

    # Test different valid datetime inputs
    dt2 = backend_utils.typecast_time(datetime.time(0, 0, 0))
    assert _sqlite_time_trunc('hour', dt2) == "00:00:00"
    
    dt3 = backend_utils.typecast_time(datetime.time(23, 45, 59))
    assert _sqlite_time_trunc('minute', dt3) == "23:45:00"
    assert _sqlite_time_trunc('second', dt3) == "23:45:59"

    # Test with unexpected lookup_type
    with pytest.raises(KeyError):
        _sqlite_time_trunc('invalid_lookup', dt)