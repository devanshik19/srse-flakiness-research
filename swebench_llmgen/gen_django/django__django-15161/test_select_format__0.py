import pytest
from django.db.models import Value, IntegerField
from django.db.models.expressions import BaseExpression
from django.db.models import Q
from django.contrib.auth.models import User


class CustomExpression(BaseExpression):
    def __init__(self, output_field=None):
        super().__init__(output_field)

    def as_sql(self, compiler, connection):
        return 'SELECT *', []


@pytest.mark.parametrize("has_select_format, expected_sql", [
    (False, ('SELECT *', [])),
    (True, ('SELECT custom_format', [])),
])
def test_select_format(has_select_format, expected_sql):
    class MockOutputField:
        def __init__(self, has_format):
            self.has_format = has_format

        def select_format(self, compiler, sql, params):
            return 'SELECT custom_format', params

    expression = CustomExpression(output_field=MockOutputField(has_select_format))
    compiler = None  # Placeholder for actual compiler
    sql, params = expression.select_format(compiler, 'SELECT *', [])
    
    assert (sql, params) == expected_sql


def test_select_format_no_output_field():
    expression = CustomExpression()
    compiler = None  # Placeholder for actual compiler
    sql, params = expression.select_format(compiler, 'SELECT *', [])
    
    assert (sql, params) == ('SELECT *', [])