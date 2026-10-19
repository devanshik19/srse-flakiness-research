import pytest
import datetime
from django.db.backends import utils as backend_utils
from django.db.backends.sqlite3.base import _sqlite_time_trunc

@pytest.mark.parametrize("lookup_type, dt, expected", [
    ('hour', datetime.time(12, 34, 56), "12:00:00"),
    ('minute', datetime.time(12, 34, 56), "12:34:00"),
    ('second', datetime.time(12, 34, 56), "12:34:56"),
    ('hour', None, None),
    ('minute', None, None),
    ('second', None, None),
    ('hour', 'not_a_time', None),
    ('minute', 'not_a_time', None),
    ('second', 'not_a_time', None),
])
def test_sqlite_time_trunc(lookup_type, dt, expected):
    result = _sqlite_time_trunc(lookup_type, dt)
    assert result == expected