import pytest
from django.db.backends.sqlite3.operations import DatabaseOperations

@pytest.mark.parametrize("lookup_type, field_name, expected_sql", [
    ("year", "created_at", "django_date_trunc('year', created_at)"),
    ("month", "updated_at", "django_date_trunc('month', updated_at)"),
    ("day", "last_login", "django_date_trunc('day', last_login)"),
    ("hour", "created_at", "django_date_trunc('hour', created_at)"),
])
def test_date_trunc_sql(lookup_type, field_name, expected_sql):
    operations = DatabaseOperations()
    sql = operations.date_trunc_sql(lookup_type, field_name)
    assert sql == expected_sql