import pytest
from django.db.backends.sqlite3.operations import DatabaseOperations

@pytest.mark.parametrize("lookup_type, field_name, expected", [
    ("day", "created_at", "django_date_trunc('day', created_at)"),
    ("MONTH", "updated_at", "django_date_trunc('month', updated_at)"),
    ("YEAR", "last_login", "django_date_trunc('year', last_login)"),
])
def test_date_trunc_sql(lookup_type, field_name, expected):
    ops = DatabaseOperations()
    result = ops.date_trunc_sql(lookup_type, field_name)
    assert result == expected