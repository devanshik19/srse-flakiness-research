import pytest
from django.db.models import Expression, F
from django.contrib.auth.models import User

class TestBaseExpression(Expression):
    def get_source_expressions(self):
        return [self]

    @property
    def contains_aggregate(self):
        return False

def test_get_group_by_cols_no_aggregate():
    expr = TestBaseExpression()
    result = expr.get_group_by_cols()
    assert result == [expr]

class TestAggregateExpression(TestBaseExpression):
    @property
    def contains_aggregate(self):
        return True

def test_get_group_by_cols_with_aggregate():
    user_expr = TestBaseExpression()
    aggregate_expr = TestAggregateExpression()
    user_expr.set_source_expressions([aggregate_expr])
    result = user_expr.get_group_by_cols()
    assert result == [aggregate_expr]