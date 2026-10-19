import pytest
from django.db.backends.sqlite3.operations import DatabaseOperations

class TestDatabaseOperations:
    def setup_method(self):
        self.operations = DatabaseOperations()

    def test_date_extract_sql(self):
        lookup_type = 'year'
        field_name = 'created_at'
        expected_sql = "django_date_extract('year', created_at)"
        
        result = self.operations.date_extract_sql(lookup_type, field_name)
        
        assert result == expected_sql

    def test_date_extract_sql_lowercase(self):
        lookup_type = 'MONTH'
        field_name = 'created_at'
        expected_sql = "django_date_extract('month', created_at)"
        
        result = self.operations.date_extract_sql(lookup_type, field_name)
        
        assert result == expected_sql

    def test_date_extract_sql_field_name(self):
        lookup_type = 'day'
        field_name = 'user__last_login'
        expected_sql = "django_date_extract('day', user__last_login)"
        
        result = self.operations.date_extract_sql(lookup_type, field_name)
        
        assert result == expected_sql