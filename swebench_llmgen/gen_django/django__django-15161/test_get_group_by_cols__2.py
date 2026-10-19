import pytest
from django.db.models import F
from django.contrib.auth.models import User
from django.db.models.expressions import BaseExpression

class TestBaseExpression(BaseExpression):

    def get_source_expressions(self):
        return [F('id')]

    def contains_aggregate(self):
        return False

def test_get_group_by_cols_without_aggregate():
    expr = TestBaseExpression(output_field=None)
    result = expr.get_group_by_cols()
    
    assert len(result) == 1
    assert result[0] == expr

def test_get_group_by_cols_with_aggregate():
    class AggregateExpression(TestBaseExpression):
        def contains_aggregate(self):
            return True

        def get_source_expressions(self):
            return [TestBaseExpression(output_field=None), TestBaseExpression(output_field=None)]

    expr = AggregateExpression(output_field=None)
    result = expr.get_group_by_cols()

    assert len(result) == 2
    assert result[0] != result[1]