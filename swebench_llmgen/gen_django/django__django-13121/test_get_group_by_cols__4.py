import pytest
from django.db.models import F
from django.contrib.auth.models import User
from django.db.models.expressions import BaseExpression

class TestBaseExpression(BaseExpression):
    def get_source_expressions(self):
        return [self]

    @property
    def contains_aggregate(self):
        return False

def test_get_group_by_cols_without_aggregate():
    expression = TestBaseExpression(output_field=None)
    result = expression.get_group_by_cols()

    assert result == [expression]

def test_get_group_by_cols_with_aggregate():
    class AggregateExpression(TestBaseExpression):
        @property
        def contains_aggregate(self):
            return True

        def get_source_expressions(self):
            return [TestBaseExpression(output_field=None), TestBaseExpression(output_field=None)]

    expression = AggregateExpression(output_field=None)
    result = expression.get_group_by_cols()

    assert len(result) == 2
    assert result[0] is not None
    assert result[1] is not None