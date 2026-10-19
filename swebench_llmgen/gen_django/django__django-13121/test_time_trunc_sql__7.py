import pytest
from django.contrib.auth.models import User
from django.db.backends.mysql.operations import DatabaseOperations

def test_time_trunc_sql():
    db_ops = DatabaseOperations()
    
    # Test with 'hour'
    result = db_ops.time_trunc_sql('hour', 'created_at')
    expected = "CAST(DATE_FORMAT(created_at, '%%H:00:00') AS TIME)"
    assert result == expected

    # Test with 'minute'
    result = db_ops.time_trunc_sql('minute', 'created_at')
    expected = "CAST(DATE_FORMAT(created_at, '%%H:%%i:00') AS TIME)"
    assert result == expected

    # Test with 'second'
    result = db_ops.time_trunc_sql('second', 'created_at')
    expected = "CAST(DATE_FORMAT(created_at, '%%H:%%i:%%s') AS TIME)"
    assert result == expected

    # Test with an invalid `lookup_type`
    result = db_ops.time_trunc_sql('day', 'created_at')
    expected = "TIME(created_at)"
    assert result == expected