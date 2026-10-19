import pytest
from django.db.backends.mysql.operations import DatabaseOperations

@pytest.mark.parametrize("lookup_type, field_name, expected_sql", [
    ('hour', 'field', "CAST(DATE_FORMAT(field, '%%H:00:00') AS TIME)"),
    ('minute', 'field', "CAST(DATE_FORMAT(field, '%%H:%%i:00') AS TIME)"),
    ('second', 'field', "CAST(DATE_FORMAT(field, '%%H:%%i:%%s') AS TIME)"),
    ('day', 'field', "TIME(field)"),
])
def test_time_trunc_sql(lookup_type, field_name, expected_sql):
    db_ops = DatabaseOperations()
    sql = db_ops.time_trunc_sql(lookup_type, field_name)
    assert sql == expected_sql