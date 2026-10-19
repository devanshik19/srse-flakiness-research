import pytest
from django.contrib.auth.models import User
from django.db.backends.mysql.operations import DatabaseOperations

@pytest.mark.parametrize("lookup_type, expected_sql", [
    ('hour', "CAST(DATE_FORMAT(%s, '%H:00:00') AS TIME)"),
    ('minute', "CAST(DATE_FORMAT(%s, '%H:%i:00') AS TIME)"),
    ('second', "CAST(DATE_FORMAT(%s, '%H:%i:%s') AS TIME)"),
    ('invalid', "TIME(%s)"),
])
def test_time_trunc_sql(lookup_type, expected_sql):
    db_operations = DatabaseOperations()
    field_name = "created_at"  # Assuming 'created_at' is a datetime field in User model.

    sql = db_operations.time_trunc_sql(lookup_type, field_name)

    # Check if the returned SQL matches the expected pattern
    assert sql == expected_sql % field_name