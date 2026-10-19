import pytest
from django.db.models.expressions import BaseExpression
from django.contrib.auth.models import User
from django.db.models.sql.compiler import SQLCompiler

class TestBaseExpression(BaseExpression):
    def __init__(self, output_field):
        super().__init__(output_field)

    def as_sql(self, compiler, connection):
        return "SELECT * FROM auth_user", []

def test_as_sql():
    # Arrange
    mock_output_field = None  # Replace with appropriate output_field if needed
    expression = TestBaseExpression(output_field=mock_output_field)
    
    # Mock compiler
    class MockCompiler(SQLCompiler):
        def compile(self, sql, params=None):
            return sql, params or []

    mock_compiler = MockCompiler(None, None, None, None)
    mock_connection = None  # the connection is not used in the base method
    
    # Act
    sql, params = expression.as_sql(mock_compiler, mock_connection)

    # Assert
    assert sql == "SELECT * FROM auth_user"
    assert params == []