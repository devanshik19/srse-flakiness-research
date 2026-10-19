import pytest
from django.contrib.auth.models import User
from django.db.models import ExpressionWrapper, F
from django.db.models.expressions import BaseExpression

class TestBaseExpression(BaseExpression):

    def contains_aggregate(self):
        return False

    def get_source_expressions(self):
        return []

def test_get_group_by_cols_no_aggregate():
    expr = TestBaseExpression()
    result = expr.get_group_by_cols()
    assert result == [expr]

def test_get_group_by_cols_with_aggregate():
    class AggregateExpression(TestBaseExpression):
        def contains_aggregate(self):
            return True
        
        def get_source_expressions(self):
            return [TestBaseExpression(), TestBaseExpression()]

    expr = AggregateExpression()
    result = expr.get_group_by_cols()
    assert len(result) == 2
    assert result[0] != result[1]  # Ensure they are distinct expressions
    assert all(isinstance(col, TestBaseExpression) for col in result)

def test_get_group_by_cols_nested():
    class NestedExpression(TestBaseExpression):
        def contains_aggregate(self):
            return True
        
        def get_source_expressions(self):
            return [AggregateExpression(), BaseExpression()]

    expr = NestedExpression()
    result = expr.get_group_by_cols()
    assert len(result) == 3
    assert isinstance(result[0], AggregateExpression)
    assert isinstance(result[1], TestBaseExpression)
    assert isinstance(result[2], BaseExpression)