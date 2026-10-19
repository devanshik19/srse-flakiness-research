import pytest
from django.db.backends.sqlite3.operations import DatabaseOperations

class TestDatabaseOperations:
    @pytest.fixture
    def db_operations(self):
        return DatabaseOperations()

    def test_date_trunc_sql(self, db_operations):
        # Test with various lookup types
        result = db_operations.date_trunc_sql('day', 'some_field')
        assert result == "django_date_trunc('day', some_field)"

        result = db_operations.date_trunc_sql('month', 'another_field')
        assert result == "django_date_trunc('month', another_field)"

        result = db_operations.date_trunc_sql('Year', 'third_field')
        assert result == "django_date_trunc('year', third_field)"

        # Test with some edge cases
        result = db_operations.date_trunc_sql('', 'field_without_lookup')
        assert result == "django_date_trunc('', field_without_lookup)"

        result = db_operations.date_trunc_sql('  ', 'field_with_spaces')
        assert result == "django_date_trunc('  ', field_with_spaces)"