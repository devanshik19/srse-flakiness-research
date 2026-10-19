import pytest
from django.db.backends.sqlite3.operations import DatabaseOperations

class TestDatabaseOperations:
    
    def setup_method(self):
        self.operations = DatabaseOperations()
    
    def test_date_extract_sql(self):
        # Test with valid lookup_type and field_name
        lookup_type = 'year'
        field_name = 'birth_date'
        expected_sql = "django_date_extract('year', birth_date)"
        
        sql = self.operations.date_extract_sql(lookup_type, field_name)
        assert sql == expected_sql
        
        # Test with different lookup_type
        lookup_type = 'MONTH'
        expected_sql = "django_date_extract('month', birth_date)"
        
        sql = self.operations.date_extract_sql(lookup_type, field_name)
        assert sql == expected_sql
        
        # Test with edge case: empty field_name
        field_name = ''
        expected_sql = "django_date_extract('year', )"
        
        sql = self.operations.date_extract_sql(lookup_type, field_name)
        assert sql == expected_sql
        
        # Test with another lookup_type
        lookup_type = 'DAY'
        expected_sql = "django_date_extract('day', birth_date)"
        
        sql = self.operations.date_extract_sql(lookup_type, field_name)
        assert sql == expected_sql
        
        # Test with a lookup_type that includes special characters
        lookup_type = 'WEEK'
        expected_sql = "django_date_extract('week', birth_date)"
        
        sql = self.operations.date_extract_sql(lookup_type, field_name)
        assert sql == expected_sql