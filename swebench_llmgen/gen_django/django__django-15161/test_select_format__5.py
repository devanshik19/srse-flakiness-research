import pytest
from django.db.models import F
from django.contrib.auth.models import User
from django.db.models.expressions import BaseExpression


class TestBaseExpression(BaseExpression):
    def __init__(self, output_field):
        super().__init__(output_field)
        
    # Necessary structure to test the select_format method
    @property
    def output_field(self):
        return self

    def select_format(self, compiler, sql, params):
        return super().select_format(compiler, sql, params)


class MockOutputField:
    def select_format(self, compiler, sql, params):
        return f"FORMATTED {sql}", params


def test_select_format_with_custom_output_field():
    # Arrange
    mock_output_field = MockOutputField()
    expression = TestBaseExpression(output_field=mock_output_field)
    sql = "SELECT * FROM auth_user"
    params = []

    # Act
    formatted_sql, formatted_params = expression.select_format(None, sql, params)

    # Assert
    assert formatted_sql == "FORMATTED SELECT * FROM auth_user"
    assert formatted_params == []


def test_select_format_without_custom_output_field():
    # Arrange
    expression = TestBaseExpression(output_field=None)
    sql = "SELECT * FROM auth_user"
    params = []

    # Act
    formatted_sql, formatted_params = expression.select_format(None, sql, params)

    # Assert
    assert formatted_sql == sql
    assert formatted_params == params