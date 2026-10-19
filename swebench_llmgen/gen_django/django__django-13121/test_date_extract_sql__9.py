import pytest
from django.db.backends.sqlite3.operations import DatabaseOperations

@pytest.mark.parametrize("lookup_type, field_name, expected", [
    ('year', 'date_field', "django_date_extract('year', date_field)"),
    ('month', 'date_field', "django_date_extract('month', date_field)"),
    ('day', 'date_field', "django_date_extract('day', date_field)"),
    ('hour', 'date_field', "django_date_extract('hour', date_field)"),
    ('minute', 'date_field', "django_date_extract('minute', date_field)"),
    ('second', 'date_field', "django_date_extract('second', date_field)"),
])
def test_date_extract_sql(lookup_type, field_name, expected):
    ops = DatabaseOperations()
    result = ops.date_extract_sql(lookup_type, field_name)
    assert result == expected