import pytest
from django.db.models import F
from django.contrib.auth.models import User
from django.db.models.expressions import BaseExpression

class TestBaseExpression(BaseExpression):

    def get_source_expressions(self):
        # Assuming the source expressions return a list of self for the mock
        return [self]

    def contains_aggregate(self):
        return False

def test_get_group_by_cols_no_aggregate():
    expr = TestBaseExpression(output_field=None)
    result = expr.get_group_by_cols()
    assert result == [expr]

def test_get_group_by_cols_with_aggregate():
    class TestAggregateExpression(BaseExpression):
        def contains_aggregate(self):
            return True

        def get_source_expressions(self):
            return [TestBaseExpression(output_field=None), TestBaseExpression(output_field=None)]

    expr = TestAggregateExpression(output_field=None)
    result = expr.get_group_by_cols()
    assert len(result) == 2
    assert all(isinstance(col, TestBaseExpression) for col in result)