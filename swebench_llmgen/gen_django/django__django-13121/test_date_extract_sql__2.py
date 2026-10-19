import pytest
from django.db.backends.sqlite3.operations import DatabaseOperations

class TestDatabaseOperations:
    def setup_method(self):
        self.ops = DatabaseOperations()

    def test_date_extract_sql(self):
        # Test with a lookup_type that should be converted to lower case
        result = self.ops.date_extract_sql('YEAR', 'birth_date')
        assert result == "django_date_extract('year', birth_date)"

        # Test with another lookup_type
        result = self.ops.date_extract_sql('MONTH', 'created_at')
        assert result == "django_date_extract('month', created_at)"

        # Test with a different field name
        result = self.ops.date_extract_sql('DAY', 'event_date')
        assert result == "django_date_extract('day', event_date)"