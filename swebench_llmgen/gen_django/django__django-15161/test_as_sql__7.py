import pytest
from django.db import connection
from django.db.models import Expression
from django.contrib.auth.models import User

class TestBaseExpression(Expression):
    def as_sql(self, compiler, connection):
        # A simple mock implementation that needs to be overridden in the test.
        return "SELECT * FROM auth_user", []

def test_as_sql_not_implemented():
    with pytest.raises(NotImplementedError, match="Subclasses must implement as_sql()"):
        expr = Expression()
        expr.as_sql(None, None)

def test_as_sql_with_mocked_expression():
    expr = TestBaseExpression()
    sql, params = expr.as_sql(None, connection)
    
    assert sql == "SELECT * FROM auth_user"
    assert params == []

def test_as_sql_subclass_override():
    class CustomExpression(TestBaseExpression):
        def as_sql(self, compiler, connection):
            return "SELECT username FROM auth_user", []

    custom_expr = CustomExpression()
    sql, params = custom_expr.as_sql(None, connection)
    
    assert sql == "SELECT username FROM auth_user"
    assert params == []