import pytest
from django.db.models import F
from django.contrib.auth.models import User
from django.db import connection
from django.db.models.expressions import BaseExpression

class TestBaseExpression(BaseExpression):

    def as_sql(self, compiler, connection):
        """
        Implementing a simple as_sql for testing purposes.
        Just returns a simple SQL and parameters.
        """
        return ('SELECT * FROM auth_user', [])

def test_as_sql():
    expression = TestBaseExpression(output_field=F('username'))
    
    # Create a dummy compiler
    class DummyCompiler:
        def compile(self, value):
            return value

        def quote(self, value):
            return f"'{value}'"

    compiler = DummyCompiler()
    
    sql, params = expression.as_sql(compiler, connection)
    
    assert sql == 'SELECT * FROM auth_user'
    assert params == []

def test_as_sql_not_implemented():
    with pytest.raises(NotImplementedError, match="Subclasses must implement as_sql()"):
        BaseExpression().as_sql(None, None)