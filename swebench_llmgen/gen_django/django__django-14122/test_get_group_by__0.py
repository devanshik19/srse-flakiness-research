import pytest
from django.db import models
from django.contrib.auth.models import User
from django.db.models.sql.compiler import SQLCompiler

@pytest.mark.parametrize(
    "query_group_by, select, order_by, expected",
    [
        (None, [], [], []),
        (True, [], [("username", None, True)], [("username", [])]),
        (["username"], [("username", None, True)], [("id", None, False)], [("username", []), ("id", [])]),
        (["username", "id"], [("username", None, True)], [], [("username", []), ("id", [])]),
        (["username"], [], [("email", None, False)], [("username", []), ("email", [])]),
        (None, [], [("username", None, True)], []),
    ]
)
def test_get_group_by(query_group_by, select, order_by, expected):
    # Mocking the SQLCompiler
    class MockQuery:
        group_by = query_group_by

    class MockSQLCompiler(SQLCompiler):
        def __init__(self, query):
            self.query = query
            self.having = None  # Adjust as necessary for conditions on HAVING

        def compile(self, expr):
            return str(expr), []  # Mock compile method

        def collapse_group_by(self, expressions, having):
            return list(dict.fromkeys(expressions))  # Unique expressions

    mock_query = MockQuery()
    compiler = MockSQLCompiler(mock_query)
    
    # Override the required methods for testing
    compiler.get_group_by_cols = lambda: [F("username"), F("email"), F("id")]
    
    result = compiler.get_group_by(select, order_by)
    
    assert result == expected