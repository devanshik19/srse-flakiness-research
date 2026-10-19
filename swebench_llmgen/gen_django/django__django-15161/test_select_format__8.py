import pytest
from django.db.models.expressions import BaseExpression
from django.db.models import IntegerField
from django.db.backends.utils import CursorWrapper

class MockOutputField:
    def select_format(self, compiler, sql, params):
        return f"SELECT {sql}", params

class MockCompiler:
    pass

def test_select_format_with_custom_output_field():
    # Arrange
    expression = BaseExpression(output_field=MockOutputField())
    compiler = MockCompiler()
    sql = "my_column"
    params = []

    # Act
    result_sql, result_params = expression.select_format(compiler, sql, params)

    # Assert
    assert result_sql == "SELECT my_column"
    assert result_params == params

def test_select_format_without_custom_output_field():
    # Arrange
    expression = BaseExpression(output_field=IntegerField())
    compiler = MockCompiler()
    sql = "my_column"
    params = []

    # Act
    result_sql, result_params = expression.select_format(compiler, sql, params)

    # Assert
    assert result_sql == sql
    assert result_params == params