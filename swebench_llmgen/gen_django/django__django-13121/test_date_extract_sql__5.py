import pytest
from django.db.backends.sqlite3.operations import DatabaseOperations

class TestDatabaseOperations:

    @pytest.fixture
    def db_operations(self):
        return DatabaseOperations()

    def test_date_extract_sql(self, db_operations):
        # Test with different lookup types
        assert db_operations.date_extract_sql('YEAR', 'created_at') == "django_date_extract('year', created_at)"
        assert db_operations.date_extract_sql('MONTH', 'created_at') == "django_date_extract('month', created_at)"
        assert db_operations.date_extract_sql('DAY', 'created_at') == "django_date_extract('day', created_at)"
        
        # Test with input that requires lowercasing lookup_type
        assert db_operations.date_extract_sql('Quarter', 'updated_at') == "django_date_extract('quarter', updated_at)"

        # Test with actual field names that might be used in a database call
        assert db_operations.date_extract_sql('WEEK', 'registration_date') == "django_date_extract('week', registration_date)"
        assert db_operations.date_extract_sql('Hour', 'last_login') == "django_date_extract('hour', last_login)"