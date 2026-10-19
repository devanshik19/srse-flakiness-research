import pytest
from django.db.backends.sqlite3.operations import DatabaseOperations

class TestDatabaseOperations:

    def setup_method(self):
        self.operations = DatabaseOperations()

    def test_date_extract_sql(self):
        # Test for standard lookup type and field name
        lookup_type = 'YEAR'
        field_name = 'date_field'
        expected_sql = "django_date_extract('year', date_field)"
        assert self.operations.date_extract_sql(lookup_type, field_name) == expected_sql

    def test_date_extract_sql_lowercase_lookup_type(self):
        # Test with lowercase lookup type
        lookup_type = 'month'
        field_name = 'date_field'
        expected_sql = "django_date_extract('month', date_field)"
        assert self.operations.date_extract_sql(lookup_type, field_name) == expected_sql

    def test_date_extract_sql_empty_field_name(self):
        # Test with empty field name
        lookup_type = 'DAY'
        field_name = ''
        expected_sql = "django_date_extract('day', )"
        assert self.operations.date_extract_sql(lookup_type, field_name) == expected_sql

    def test_date_extract_sql_special_characters(self):
        # Test with special characters in field name
        lookup_type = 'HOUR'
        field_name = 'date_field_@#'
        expected_sql = "django_date_extract('hour', date_field_@#)"
        assert self.operations.date_extract_sql(lookup_type, field_name) == expected_sql