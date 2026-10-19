import pytest
import datetime
from django.db.backends import utils as backend_utils
from django.contrib.auth.models import User
from django.db.utils import ProgrammingError

# Assuming the function _sqlite_time_trunc is in the same module as the imports
from django.db.backends.sqlite3.base import _sqlite_time_trunc

def test_sqlite_time_trunc():
    # Test with None
    assert _sqlite_time_trunc('hour', None) is None
    assert _sqlite_time_trunc('minute', None) is None
    assert _sqlite_time_trunc('second', None) is None

    # Test with valid datetime input
    dt = backend_utils.typecast_time(datetime.datetime(2023, 10, 10, 12, 30, 45))
    
    assert _sqlite_time_trunc('hour', dt) == "12:00:00"
    assert _sqlite_time_trunc('minute', dt) == "12:30:00"
    assert _sqlite_time_trunc('second', dt) == "12:30:45"

    # Test with invalid datetime input
    with pytest.raises((ValueError, TypeError)):
        _sqlite_time_trunc('hour', 'invalid_datetime')

    with pytest.raises((ValueError, TypeError)):
        _sqlite_time_trunc('minute', 'invalid_datetime')

    with pytest.raises((ValueError, TypeError)):
        _sqlite_time_trunc('second', 'invalid_datetime')