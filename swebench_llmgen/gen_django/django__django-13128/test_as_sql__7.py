import pytest
from django.db import connection
from django.db.models import Expression
from django.contrib.auth.models import User

class TestBaseExpression(Expression):
    def as_sql(self, compiler, connection):
        return "SELECT * FROM auth_user", []

def test_base_expression_as_sql():
    expression = TestBaseExpression(output_field=None)
    
    # Mocked compiler
    class MockCompiler:
        def compile(self, value):
            return f'"{value}"', []

    compiler = MockCompiler()
    
    sql, params = expression.as_sql(compiler, connection)
    assert sql == 'SELECT * FROM auth_user'
    assert params == []

    with pytest.raises(NotImplementedError):
        expression_with_not_implemented = BaseExpression()
        expression_with_not_implemented.as_sql(compiler, connection)