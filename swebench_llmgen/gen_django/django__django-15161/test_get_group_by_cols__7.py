import pytest
from django.db.models import F
from django.contrib.auth.models import User
from django.db.models.expressions import BaseExpression

class TestBaseExpression(BaseExpression):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.source_expressions = []

    def get_source_expressions(self):
        return self.source_expressions

    def contains_aggregate(self):
        return False

def test_get_group_by_cols_no_aggregate():
    expr = TestBaseExpression()
    result = expr.get_group_by_cols()
    assert result == [expr]

def test_get_group_by_cols_with_aggregate():
    expr1 = TestBaseExpression()
    expr2 = TestBaseExpression()
    expr1.source_expressions = [expr2]
    
    # Simulate contains_aggregate returning True
    def contains_aggregate_override(self):
        return True

    expr1.contains_aggregate = functools.partial(contains_aggregate_override, expr1)
    expr2.contains_aggregate = functools.partial(contains_aggregate_override, expr2)
    
    result = expr1.get_group_by_cols()
    assert result == [expr2]