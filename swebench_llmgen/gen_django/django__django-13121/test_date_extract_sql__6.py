import pytest
from django.db.backends.sqlite3.operations import DatabaseOperations

@pytest.mark.parametrize("lookup_type, field_name, expected_output", [
    ("YEAR", "created_at", "django_date_extract('year', created_at)"),
    ("MONTH", "user_id", "django_date_extract('month', user_id)"),
    ("DAY", "last_login", "django_date_extract('day', last_login)"),
])
def test_date_extract_sql(lookup_type, field_name, expected_output):
    db_ops = DatabaseOperations()
    sql = db_ops.date_extract_sql(lookup_type, field_name)
    assert sql == expected_output