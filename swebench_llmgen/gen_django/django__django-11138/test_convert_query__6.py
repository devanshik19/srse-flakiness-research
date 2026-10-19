import pytest
from django.contrib.auth.models import User
from django.db.backends.sqlite3.base import SQLiteCursorWrapper

@pytest.fixture
def cursor_wrapper():
    return SQLiteCursorWrapper()

def test_convert_query(cursor_wrapper):
    # Test with a query having placeholders
    query_with_placeholders = "SELECT * FROM users WHERE username = %s AND age > %s"
    expected_output = "SELECT * FROM users WHERE username = ? AND age > ?"
    assert cursor_wrapper.convert_query(query_with_placeholders) == expected_output

    # Test with double percentage signs
    query_with_double_percentage = "SELECT * FROM users WHERE username LIKE '%%username%%'"
    expected_output_double = "SELECT * FROM users WHERE username LIKE '%username%'"
    assert cursor_wrapper.convert_query(query_with_double_percentage) == expected_output_double

    # Test with no placeholders
    query_without_placeholders = "SELECT * FROM users"
    expected_output_no_placeholders = "SELECT * FROM users"
    assert cursor_wrapper.convert_query(query_without_placeholders) == expected_output_no_placeholders

    # Test with empty query
    empty_query = ""
    assert cursor_wrapper.convert_query(empty_query) == ""

    # Test with only placeholders
    only_placeholders_query = "%s %s %s"
    expected_output_only_placeholders = "? ? ?"
    assert cursor_wrapper.convert_query(only_placeholders_query) == expected_output_only_placeholders