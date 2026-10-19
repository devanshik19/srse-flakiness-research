import pytest
from django.db.backends.sqlite3.operations import DatabaseOperations

@pytest.mark.parametrize("lookup_type, field_name, expected", [
    ('year', 'created_at', "django_date_trunc('year', created_at)"),
    ('month', 'updated_at', "django_date_trunc('month', updated_at)"),
    ('day', 'login_time', "django_date_trunc('day', login_time)"),
])
def test_date_trunc_sql(lookup_type, field_name, expected):
    operations = DatabaseOperations()
    sql = operations.date_trunc_sql(lookup_type, field_name)
    assert sql == expected