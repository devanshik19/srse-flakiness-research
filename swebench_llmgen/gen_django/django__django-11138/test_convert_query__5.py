import pytest
import re
from django.contrib.auth.models import User
from django.db.backends.sqlite3.base import SQLiteCursorWrapper

# Define FORMAT_QMARK_REGEX as used in the original context
FORMAT_QMARK_REGEX = re.compile(r'\?')

@pytest.fixture
def cursor_wrapper():
    return SQLiteCursorWrapper()

def test_convert_query_single_placeholder(cursor_wrapper):
    query = "SELECT * FROM my_table WHERE id = ?"
    expected = "SELECT * FROM my_table WHERE id = ?"
    assert cursor_wrapper.convert_query(query) == expected

def test_convert_query_double_placeholder(cursor_wrapper):
    query = "SELECT * FROM my_table WHERE id = ? AND name = ?"
    expected = "SELECT * FROM my_table WHERE id = ? AND name = ?"
    assert cursor_wrapper.convert_query(query) == expected

def test_convert_query_percentage_sign(cursor_wrapper):
    query = "SELECT * FROM my_table WHERE name LIKE '%%john%%'"
    expected = "SELECT * FROM my_table WHERE name LIKE '%john%'"
    assert cursor_wrapper.convert_query(query) == expected

def test_convert_query_multiple_percentage_signs(cursor_wrapper):
    query = "SELECT * FROM my_table WHERE name LIKE '%%john%%' AND email LIKE '%%example.com%%'"
    expected = "SELECT * FROM my_table WHERE name LIKE '%john%' AND email LIKE '%example.com%'"
    assert cursor_wrapper.convert_query(query) == expected

def test_convert_query_no_placeholders(cursor_wrapper):
    query = "SELECT * FROM my_table"
    expected = "SELECT * FROM my_table"
    assert cursor_wrapper.convert_query(query) == expected

def test_convert_query_only_placeholders(cursor_wrapper):
    query = "??"
    expected = "??"
    assert cursor_wrapper.convert_query(query) == expected