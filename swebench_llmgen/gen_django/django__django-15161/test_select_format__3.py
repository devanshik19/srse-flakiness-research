import pytest
from django.db.models import F
from django.contrib.auth.models import User
from django.db.models.expressions import BaseExpression


class CustomField:
    def select_format(self, compiler, sql, params):
        return f"Formatted: {sql}", params


def test_select_format_with_custom_field():
    # Arrange
    user = User.objects.create_user(username='testuser', password='password')
    expression = BaseExpression(output_field=CustomField())
    sql = "SELECT * FROM auth_user"
    params = []

    # Act
    formatted_sql, formatted_params = expression.select_format(None, sql, params)

    # Assert
    assert formatted_sql == "Formatted: SELECT * FROM auth_user"
    assert formatted_params == params


def test_select_format_without_custom_field():
    # Arrange
    user = User.objects.create_user(username='testuser', password='password')
    expression = BaseExpression(output_field=F('username'))
    sql = "SELECT * FROM auth_user"
    params = []

    # Act
    formatted_sql, formatted_params = expression.select_format(None, sql, params)

    # Assert
    assert formatted_sql == sql
    assert formatted_params == params