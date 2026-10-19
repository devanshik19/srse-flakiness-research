import pytest
from django.db.backends.sqlite3.base import SQLiteCursorWrapper

class TestSQLiteCursorWrapper:

    @pytest.fixture
    def cursor_wrapper(self):
        return SQLiteCursorWrapper()

    def test_convert_query_single_placeholder(self, cursor_wrapper):
        query = "SELECT * FROM users WHERE id = %s"
        expected = "SELECT * FROM users WHERE id = ?"
        assert cursor_wrapper.convert_query(query) == expected

    def test_convert_query_double_percent(self, cursor_wrapper):
        query = "SELECT * FROM users WHERE name LIKE '%%s'"
        expected = "SELECT * FROM users WHERE name LIKE '%s'"
        assert cursor_wrapper.convert_query(query) == expected

    def test_convert_query_no_placeholder(self, cursor_wrapper):
        query = "SELECT * FROM users"
        expected = "SELECT * FROM users"
        assert cursor_wrapper.convert_query(query) == expected

    def test_convert_query_multiple_placeholders(self, cursor_wrapper):
        query = "SELECT * FROM users WHERE id = %s AND age > %s"
        expected = "SELECT * FROM users WHERE id = ? AND age > ?"
        assert cursor_wrapper.convert_query(query) == expected

    def test_convert_query_edge_case_double_percent(self, cursor_wrapper):
        query = "SELECT * FROM users WHERE name LIKE '%%' OR id = %s"
        expected = "SELECT * FROM users WHERE name LIKE '%' OR id = ?"
        assert cursor_wrapper.convert_query(query) == expected

    def test_convert_query_no_changes_needed(self, cursor_wrapper):
        query = "SELECT * FROM users WHERE amount = 100"
        expected = "SELECT * FROM users WHERE amount = 100"
        assert cursor_wrapper.convert_query(query) == expected