import pytest
from django.contrib.auth.models import User
from django.db.models.expressions import BaseExpression

class TestBaseExpression(BaseExpression):
    def as_sql(self, compiler, connection):
        return 'SELECT * FROM auth_user', []

def test_base_expression_as_sql():
    # Create an instance of the test class
    expression = TestBaseExpression(output_field=None)

    # Create a mock compiler and connection
    class MockCompiler:
        def compile(self, value):
            return f'compiled_{value}'

    class MockConnection:
        vendor = 'sqlite'

    compiler = MockCompiler()
    connection = MockConnection()

    # Execute as_sql and check results
    sql, params = expression.as_sql(compiler, connection)
    
    assert sql == 'SELECT * FROM auth_user'
    assert params == []