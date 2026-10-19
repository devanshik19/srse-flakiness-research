import pytest
from django.db.backends.sqlite3.operations import DatabaseOperations

@pytest.fixture
def db_operations():
    return DatabaseOperations()

def test_date_trunc_sql(db_operations):
    # Test case 1: basic truncation
    result = db_operations.date_trunc_sql('year', 'created_at')
    expected = "django_date_trunc('year', created_at)"
    assert result == expected

    # Test case 2: lower case check for lookup type
    result = db_operations.date_trunc_sql('Month', 'updated_at')
    expected = "django_date_trunc('month', updated_at)"
    assert result == expected

    # Test case 3: testing field names with underscores
    result = db_operations.date_trunc_sql('day', 'some_field_name')
    expected = "django_date_trunc('day', some_field_name)"
    assert result == expected

    # Test case 4: testing a different lookup type
    result = db_operations.date_trunc_sql('SECOND', 'timestamp_field')
    expected = "django_date_trunc('second', timestamp_field)"
    assert result == expected