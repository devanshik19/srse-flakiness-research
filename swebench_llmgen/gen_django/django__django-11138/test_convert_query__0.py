import pytest
import re
from django.contrib.auth.models import User
from django.db.backends.sqlite3.base import SQLiteCursorWrapper

FORMAT_QMARK_REGEX = re.compile(r'\?')

class TestSQLiteCursorWrapper:

    @pytest.fixture
    def cursor_wrapper(self):
        return SQLiteCursorWrapper()

    def test_convert_query_no_placeholder(self, cursor_wrapper):
        query = "SELECT * FROM users"
        result = cursor_wrapper.convert_query(query)
        assert result == "SELECT * FROM users"

    def test_convert_query_with_placeholder(self, cursor_wrapper):
        query = "SELECT * FROM users WHERE id = ?"
        result = cursor_wrapper.convert_query(query)
        assert result == "SELECT * FROM users WHERE id = ?"

    def test_convert_query_with_double_percentage(self, cursor_wrapper):
        query = "SELECT * FROM users WHERE name LIKE '%%name%%'"
        result = cursor_wrapper.convert_query(query)
        assert result == "SELECT * FROM users WHERE name LIKE '%name%'"

    def test_convert_query_with_both_placeholders(self, cursor_wrapper):
        query = "SELECT * FROM users WHERE id = ? AND name LIKE '%%name%%'"
        result = cursor_wrapper.convert_query(query)
        assert result == "SELECT * FROM users WHERE id = ? AND name LIKE '%name%'"

    def test_convert_query_empty_string(self, cursor_wrapper):
        query = ""
        result = cursor_wrapper.convert_query(query)
        assert result == ""