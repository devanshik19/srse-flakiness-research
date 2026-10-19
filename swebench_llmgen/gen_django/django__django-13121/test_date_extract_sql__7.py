import pytest
from django.db import connection
from django.db.backends.sqlite3.operations import DatabaseOperations

@pytest.mark.parametrize("lookup_type, field_name, expected_sql", [
    ('year', 'created_at', "django_date_extract('year', created_at)"),
    ('month', 'updated_at', "django_date_extract('month', updated_at)"),
    ('day', 'last_login', "django_date_extract('day', last_login)"),
])
def test_date_extract_sql(lookup_type, field_name, expected_sql):
    ops = DatabaseOperations()
    sql = ops.date_extract_sql(lookup_type, field_name)
    assert sql == expected_sql