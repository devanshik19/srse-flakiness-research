import pytest
from django.contrib.auth.models import User
from django.db.backends.mysql.operations import DatabaseOperations

@pytest.mark.parametrize("lookup_type, expected_output", [
    ('hour', "CAST(DATE_FORMAT(%s, '%H:00:00') AS TIME)"),
    ('minute', "CAST(DATE_FORMAT(%s, '%H:%i:00') AS TIME)"),
    ('second', "CAST(DATE_FORMAT(%s, '%H:%i:%s') AS TIME)"),
    ('unknown', "TIME(%s)"),
])
def test_time_trunc_sql(lookup_type, expected_output):
    ops = DatabaseOperations()
    field_name = 'somefield'

    result = ops.time_trunc_sql(lookup_type, field_name)
    assert result == expected_output % field_name