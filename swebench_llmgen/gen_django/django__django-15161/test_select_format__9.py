import pytest
from django.db.models import F
from django.contrib.auth.models import User
from django.db.models.expressions import BaseExpression

class TestBaseExpression(BaseExpression):
    def __init__(self, output_field=None):
        super().__init__(output_field=output_field)
        self.output_field = output_field

def test_select_format_with_output_field():
    # Arrange
    user_expression = TestBaseExpression(output_field=F('username'))
    compiler = object()  # placeholder for the compiler
    sql = 'SELECT * FROM auth_user'
    params = []

    # Act
    formatted_sql, formatted_params = user_expression.select_format(compiler, sql, params)

    # Assert
    assert formatted_sql == sql
    assert formatted_params == params

def test_select_format_with_custom_output_field():
    class CustomField:
        def select_format(self, compiler, sql, params):
            return f'CASE WHEN {sql} THEN 1 ELSE 0 END', params

    # Arrange
    user_expression = TestBaseExpression(output_field=CustomField())
    compiler = object()  # placeholder for the compiler
    sql = 'SELECT * FROM auth_user'
    params = []

    # Act
    formatted_sql, formatted_params = user_expression.select_format(compiler, sql, params)

    # Assert
    assert formatted_sql == f'CASE WHEN {sql} THEN 1 ELSE 0 END'
    assert formatted_params == params

def test_select_format_without_output_field():
    # Arrange
    user_expression = TestBaseExpression(output_field=None)
    compiler = object()  # placeholder for the compiler
    sql = 'SELECT * FROM auth_user'
    params = []

    # Act
    formatted_sql, formatted_params = user_expression.select_format(compiler, sql, params)

    # Assert
    assert formatted_sql == sql
    assert formatted_params == params