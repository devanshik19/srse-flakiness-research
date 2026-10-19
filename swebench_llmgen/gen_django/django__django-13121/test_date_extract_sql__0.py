import pytest
from django.db.backends.sqlite3.operations import DatabaseOperations

class TestDatabaseOperations:

    def setup_method(self):
        self.operations = DatabaseOperations()

    def test_date_extract_sql(self):
        # Test with a standard lookup type and field name
        lookup_type = 'year'
        field_name = 'my_date_field'
        expected_sql = "django_date_extract('year', my_date_field)"
        actual_sql = self.operations.date_extract_sql(lookup_type, field_name)
        assert actual_sql == expected_sql

    def test_date_extract_sql_lowercase(self):
        # Test with varying case in lookup type
        lookup_type = 'MONTH'
        field_name = 'my_date_field'
        expected_sql = "django_date_extract('month', my_date_field)"
        actual_sql = self.operations.date_extract_sql(lookup_type, field_name)
        assert actual_sql == expected_sql

    def test_date_extract_sql_quotes(self):
        # Test with a field name that includes special characters
        lookup_type = 'day'
        field_name = '"my_date_field_with_special_chars!"'
        expected_sql = "django_date_extract('day', \"my_date_field_with_special_chars!\")"
        actual_sql = self.operations.date_extract_sql(lookup_type, field_name)
        assert actual_sql == expected_sql