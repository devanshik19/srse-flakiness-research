import pytest
from django.db.models.expressions import BaseExpression
from django.db.models import F
from django.contrib.auth.models import User


class TestSelectFormatExpression(BaseExpression):
    def __init__(self, output_field=None):
        self.output_field = output_field


@pytest.fixture
def custom_expression():
    return TestSelectFormatExpression(F('username'))


def test_select_format_with_custom_output_field(custom_expression):
    class MockOutputField:
        def select_format(self, compiler, sql, params):
            return f"SELECT * FROM users WHERE {sql}", params

    custom_expression.output_field = MockOutputField()
    sql, params = custom_expression.select_format(None, "username = %s", [User.objects.first().username])

    assert sql == "SELECT * FROM users WHERE username = %s"
    assert params == [User.objects.first().username]


def test_select_format_without_custom_output_field(custom_expression):
    custom_expression.output_field = None
    sql, params = custom_expression.select_format(None, "username = %s", [User.objects.first().username])

    assert sql == "username = %s"
    assert params == [User.objects.first().username]