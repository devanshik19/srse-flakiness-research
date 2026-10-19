import pytest
import re
from django.contrib.auth.models import User
from django.db.backends.sqlite3.base import SQLiteCursorWrapper

# Assuming the FORMAT_QMARK_REGEX is defined as it should be in the context of the class
FORMAT_QMARK_REGEX = re.compile(r'\?')

def test_convert_query():
    cursor_wrapper = SQLiteCursorWrapper()

    # Test cases
    test_cases = [
        # Test replacing FORMAT_QMARK_REGEX pattern
        ("SELECT * FROM users WHERE id = ?;", "SELECT * FROM users WHERE id = ?;"),
        # Test handling double percentage signs
        ("SELECT * FROM users WHERE name LIKE '%%John%%';", "SELECT * FROM users WHERE name LIKE '%John%';"),
        # Test a query with multiple parameters
        ("SELECT * FROM users WHERE id = ? AND name = ?;", "SELECT * FROM users WHERE id = ? AND name = ?;"),
        # Test a query which does not require replacements
        ("SELECT * FROM users;", "SELECT * FROM users;"),
        # Test replacing multiple FORMAT_QMARK_REGEX patterns and double percentage signs
        ("SELECT * FROM users WHERE age > ? AND name LIKE '%%Alice%%';", "SELECT * FROM users WHERE age > ? AND name LIKE '%Alice%';"),
    ]

    for query, expected in test_cases:
        result = cursor_wrapper.convert_query(query)
        assert result == expected