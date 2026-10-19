import pytest
from django.db.models import F
from django.contrib.auth.models import User
from django.db.models.expressions import BaseExpression

class TestBaseExpression(BaseExpression):
    def get_source_expressions(self):
        # Overriding to return a list with a single expression (itself) for testing
        return [self]

    @property
    def contains_aggregate(self):
        return False

def test_get_group_by_cols_no_aggregate():
    expr = TestBaseExpression(output_field=F('username'))
    result = expr.get_group_by_cols()
    assert result == [expr]

def test_get_group_by_cols_with_aggregate():
    class AggregateExpression(TestBaseExpression):
        @property
        def contains_aggregate(self):
            return True

        def get_source_expressions(self):
            return [TestBaseExpression(output_field=F('email')), TestBaseExpression(output_field=F('date_joined'))]

    expr = AggregateExpression(output_field=F('username'))
    result = expr.get_group_by_cols()
    assert len(result) == 3  # Should return itself + two source expressions
    assert result[0] == expr
    assert isinstance(result[1], TestBaseExpression)
    assert isinstance(result[2], TestBaseExpression)

def test_get_group_by_cols_empty_sources():
    class EmptySourceExpression(TestBaseExpression):
        def get_source_expressions(self):
            return []

    expr = EmptySourceExpression(output_field=F('username'))
    result = expr.get_group_by_cols()
    assert result == [expr]  # should return itself only since there are no sources