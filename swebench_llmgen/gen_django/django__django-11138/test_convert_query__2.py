import pytest
from django.contrib.auth.models import User
from django.db.backends.sqlite3.base import SQLiteCursorWrapper

class TestSQLiteCursorWrapper:
    
    @pytest.fixture
    def cursor_wrapper(self):
        return SQLiteCursorWrapper()

    def test_convert_query_replaces_format_placeholder(self, cursor_wrapper):
        query = "SELECT * FROM my_table WHERE id = %s"
        expected = "SELECT * FROM my_table WHERE id = ?"
        assert cursor_wrapper.convert_query(query) == expected

    def test_convert_query_replaces_double_percent(self, cursor_wrapper):
        query = "SELECT * FROM my_table WHERE percentage = %%"
        expected = "SELECT * FROM my_table WHERE percentage = %"
        assert cursor_wrapper.convert_query(query) == expected

    def test_convert_query_empty_string(self, cursor_wrapper):
        query = ""
        expected = ""
        assert cursor_wrapper.convert_query(query) == expected

    def test_convert_query_no_placeholders(self, cursor_wrapper):
        query = "SELECT * FROM my_table"
        expected = "SELECT * FROM my_table"
        assert cursor_wrapper.convert_query(query) == expected

    def test_convert_query_combined_cases(self, cursor_wrapper):
        query = "SELECT * FROM my_table WHERE id = %s AND name = %%"
        expected = "SELECT * FROM my_table WHERE id = ? AND name = %"
        assert cursor_wrapper.convert_query(query) == expected