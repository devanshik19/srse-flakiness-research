import pytest
from django.contrib.auth.models import User
from django.db.backends.sqlite3.base import SQLiteCursorWrapper

def test_convert_query():
    cursor_wrapper = SQLiteCursorWrapper()

    # Test case 1: Basic query with a single placeholder
    query1 = "SELECT * FROM users WHERE id = %s"
    expected1 = "SELECT * FROM users WHERE id = ?"
    assert cursor_wrapper.convert_query(query1) == expected1

    # Test case 2: Query with two placeholders
    query2 = "SELECT * FROM users WHERE username = %s AND email = %s"
    expected2 = "SELECT * FROM users WHERE username = ? AND email = ?"
    assert cursor_wrapper.convert_query(query2) == expected2

    # Test case 3: Query with percent signs
    query3 = "SELECT * FROM users WHERE name LIKE '%%example%%'"
    expected3 = "SELECT * FROM users WHERE name LIKE '%example%'"
    assert cursor_wrapper.convert_query(query3) == expected3

    # Test case 4: Query with multiple double percent signs
    query4 = "SELECT * FROM users WHERE amount = %%s"
    expected4 = "SELECT * FROM users WHERE amount = ?"
    assert cursor_wrapper.convert_query(query4) == expected4

    # Test case 5: Query with no placeholders
    query5 = "SELECT * FROM users"
    expected5 = "SELECT * FROM users"
    assert cursor_wrapper.convert_query(query5) == expected5

    # Test case 6: Empty query
    query6 = ""
    expected6 = ""
    assert cursor_wrapper.convert_query(query6) == expected6