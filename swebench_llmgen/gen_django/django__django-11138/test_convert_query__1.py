import pytest
import re
from django.contrib.auth.models import User
from django.db.backends.sqlite3.base import SQLiteCursorWrapper

# Assuming FORMAT_QMARK_REGEX is defined as per the context of the original module
FORMAT_QMARK_REGEX = re.compile(r'(?<!%)%(?!%)')

@pytest.fixture
def cursor_wrapper():
    return SQLiteCursorWrapper()

def test_convert_query_single_placeholder(cursor_wrapper):
    query = "SELECT * FROM users WHERE username = %s"
    expected = "SELECT * FROM users WHERE username = ?"
    assert cursor_wrapper.convert_query(query) == expected

def test_convert_query_double_percentage(cursor_wrapper):
    query = "SELECT * FROM users WHERE username LIKE 'test%%'"
    expected = "SELECT * FROM users WHERE username LIKE 'test%'"
    assert cursor_wrapper.convert_query(query) == expected

def test_convert_query_combined(cursor_wrapper):
    query = "SELECT * FROM users WHERE username = %s AND age > %%s"
    expected = "SELECT * FROM users WHERE username = ? AND age > ?"
    assert cursor_wrapper.convert_query(query) == expected

def test_convert_query_no_placeholders(cursor_wrapper):
    query = "SELECT * FROM users"
    expected = "SELECT * FROM users"
    assert cursor_wrapper.convert_query(query) == expected

def test_convert_query_only_percentage(cursor_wrapper):
    query = "SELECT * FROM users WHERE username LIKE '%%'"
    expected = "SELECT * FROM users WHERE username LIKE '%'"
    assert cursor_wrapper.convert_query(query) == expected