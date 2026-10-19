import pytest
from django.db.models.expressions import BaseExpression
from django.db.models import F
from django.contrib.auth.models import User
from django.db import connection


class TestBaseExpression(BaseExpression):
    def as_sql(self, compiler, connection):
        return "SELECT * FROM auth_user", []


def test_base_expression_as_sql():
    # Create an instance of the testable BaseExpression subclass
    expression = TestBaseExpression(output_field=F('username'))

    # Simulating a mock compiler with minimal implementation for the test
    class MockCompiler:
        def compile(self, value):
            return (value, [])

    mock_compiler = MockCompiler()
    
    # Call the as_sql method
    sql, params = expression.as_sql(mock_compiler, connection)

    # Expected values
    expected_sql = "SELECT * FROM auth_user"
    expected_params = []

    # Assert the SQL and params
    assert sql == expected_sql
    assert params == expected_params