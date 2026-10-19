import pytest
from django.db.backends.sqlite3.operations import DatabaseOperations

@pytest.mark.parametrize("lookup_type, field_name, expected_sql", [
    ('YEAR', 'my_date_field', "django_date_extract('year', my_date_field)"),
    ('MONTH', 'another_date_field', "django_date_extract('month', another_date_field)"),
    ('DAY', 'third_date_field', "django_date_extract('day', third_date_field)"),
])
def test_date_extract_sql(lookup_type, field_name, expected_sql):
    db_operations = DatabaseOperations()
    actual_sql = db_operations.date_extract_sql(lookup_type, field_name)
    assert actual_sql == expected_sql