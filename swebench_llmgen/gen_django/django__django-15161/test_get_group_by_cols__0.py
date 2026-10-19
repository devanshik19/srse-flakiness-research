import pytest
from django.db.models import F, ExpressionWrapper, Value
from django.contrib.auth.models import User
from django.db.models.expressions import BaseExpression

class TestBaseExpression(BaseExpression):
    def get_source_expressions(self):
        return [self]

    def contains_aggregate(self):
        return False

def test_get_group_by_cols_no_aggregate():
    expression = TestBaseExpression(output_field=None)
    result = expression.get_group_by_cols()

    assert len(result) == 1
    assert result[0] is expression

def test_get_group_by_cols_with_aggregate():
    expression = TestBaseExpression(output_field=None)
    # Mock contains_aggregate to return True
    expression.contains_aggregate = lambda: True
    # Mock get_source_expressions to return expressions containing themselves
    expression.get_source_expressions = lambda: [expression]

    result = expression.get_group_by_cols()

    assert len(result) == 1
    assert result[0] is expression