import pytest
from django.db.backends.sqlite3.operations import DatabaseOperations

@pytest.mark.parametrize("lookup_type, field_name, expected_sql", [
    ("year", "created_at", "django_date_trunc('year', created_at)"),
    ("MONTH", "last_login", "django_date_trunc('month', last_login)"),
    ("day", "updated_at", "django_date_trunc('day', updated_at)"),
])
def test_date_trunc_sql(lookup_type, field_name, expected_sql):
    ops = DatabaseOperations()
    sql = ops.date_trunc_sql(lookup_type, field_name)
    assert sql == expected_sql