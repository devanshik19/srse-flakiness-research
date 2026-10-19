import pytest
from django.contrib.auth.models import User
from django.db.backends.sqlite3.base import SQLiteCursorWrapper

FORMAT_QMARK_REGEX = re.compile(r'(\?|%|\*\*|%%)')

class TestSQLiteCursorWrapper:

    @pytest.fixture(autouse=True)
    def setup_method(self):
        self.cursor_wrapper = SQLiteCursorWrapper()
        
    def test_convert_query_with_placeholder(self):
        query = "SELECT * FROM users WHERE username = ?"
        expected = "SELECT * FROM users WHERE username = ?"
        result = self.cursor_wrapper.convert_query(query)
        assert result == expected

    def test_convert_query_with_percent(self):
        query = "SELECT * FROM users WHERE username LIKE 'john%%'"
        expected = "SELECT * FROM users WHERE username LIKE 'john%'"
        result = self.cursor_wrapper.convert_query(query)
        assert result == expected

    def test_convert_query_multiple_placeholders(self):
        query = "SELECT * FROM users WHERE username = ? AND age > ?"
        expected = "SELECT * FROM users WHERE username = ? AND age > ?"
        result = self.cursor_wrapper.convert_query(query)
        assert result == expected

    def test_convert_query_no_placeholders(self):
        query = "SELECT * FROM users"
        expected = "SELECT * FROM users"
        result = self.cursor_wrapper.convert_query(query)
        assert result == expected

    def test_convert_query_edge_case(self):
        query = "SELECT * FROM users WHERE age = % AND height = %%"
        expected = "SELECT * FROM users WHERE age = ? AND height = %"
        result = self.cursor_wrapper.convert_query(query)
        assert result == expected