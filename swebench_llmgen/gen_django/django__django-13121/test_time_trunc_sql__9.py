import pytest
from django.db.backends.mysql.operations import DatabaseOperations

@pytest.mark.parametrize("lookup_type, field_name, expected_sql", [
    ('hour', 'created_at', "CAST(DATE_FORMAT(created_at, '%H:00:00') AS TIME)"),
    ('minute', 'created_at', "CAST(DATE_FORMAT(created_at, '%H:%%i:00') AS TIME)"),
    ('second', 'created_at', "CAST(DATE_FORMAT(created_at, '%H:%%i:%%s') AS TIME)"),
    ('day', 'created_at', "TIME(created_at)"),
])
def test_time_trunc_sql(lookup_type, field_name, expected_sql):
    ops = DatabaseOperations()
    sql = ops.time_trunc_sql(lookup_type, field_name)
    assert sql == expected_sql