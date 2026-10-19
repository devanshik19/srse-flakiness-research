import pytest
from django.db.backends.sqlite3.operations import DatabaseOperations

@pytest.mark.parametrize("lookup_type, field_name, expected", [
    ("year", "created_at", "django_date_trunc('year', created_at)"),
    ("MONTH", "last_updated", "django_date_trunc('month', last_updated)"),
    ("day", "signup_date", "django_date_trunc('day', signup_date)"),
    ("hour", "login_time", "django_date_trunc('hour', login_time)"),
])
def test_date_trunc_sql(lookup_type, field_name, expected):
    db_ops = DatabaseOperations()
    sql = db_ops.date_trunc_sql(lookup_type, field_name)
    assert sql == expected