import pytest
from django.db.models.expressions import BaseExpression
from django.db.models import F
from django.db import connection
from django.contrib.auth.models import User

class TestBaseExpression(BaseExpression):
    def as_sql(self, compiler, connection):
        return "SELECT * FROM auth_user", []

def test_as_sql():
    # Create a dummy compiler
    class DummyCompiler:
        def compile(self, expression):
            return expression.as_sql(self, connection)

    dummy_compiler = DummyCompiler()
    expression = TestBaseExpression(output_field=None)

    # Test the as_sql method
    sql, params = dummy_compiler.compile(expression)
    
    assert sql == "SELECT * FROM auth_user"
    assert params == []

def test_not_implemented_as_sql():
    with pytest.raises(NotImplementedError):
        expression = BaseExpression(output_field=None)
        expression.as_sql(None, None)