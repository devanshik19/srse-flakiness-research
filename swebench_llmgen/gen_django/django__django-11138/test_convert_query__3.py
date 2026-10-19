import pytest
import re
from django.contrib.auth.models import User
from django.db.backends.sqlite3.base import SQLiteCursorWrapper

FORMAT_QMARK_REGEX = re.compile(r'\?')

@pytest.fixture
def cursor_wrapper():
    return SQLiteCursorWrapper()

def test_convert_query_single_placeholder(cursor_wrapper):
    query = "SELECT * FROM users WHERE id = ?"
    expected = "SELECT * FROM users WHERE id = ?"
    assert cursor_wrapper.convert_query(query) == expected

def test_convert_query_double_placeholder(cursor_wrapper):
    query = "SELECT * FROM users WHERE id = ? AND name = ?"
    expected = "SELECT * FROM users WHERE id = ? AND name = ?"
    assert cursor_wrapper.convert_query(query) == expected

def test_convert_query_percent_sign(cursor_wrapper):
    query = "SELECT * FROM users WHERE name LIKE 'John%%'"
    expected = "SELECT * FROM users WHERE name LIKE 'John%'"
    assert cursor_wrapper.convert_query(query) == expected

def test_convert_query_double_percent_sign(cursor_wrapper):
    query = "SELECT * FROM users WHERE name LIKE 'John%%%%'"
    expected = "SELECT * FROM users WHERE name LIKE 'John%%'"
    assert cursor_wrapper.convert_query(query) == expected

def test_convert_query_empty_string(cursor_wrapper):
    query = ""
    expected = ""
    assert cursor_wrapper.convert_query(query) == expected

def test_convert_query_no_placeholders(cursor_wrapper):
    query = "SELECT * FROM users"
    expected = "SELECT * FROM users"
    assert cursor_wrapper.convert_query(query) == expected