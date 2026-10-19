import pytest
from django.db.models import F
from django.db.models import Value
from django.db.models.expressions import BaseExpression
from django.contrib.auth.models import User

class TestBaseExpression(BaseExpression):
    def get_source_expressions(self):
        return [F('username'), Value(1)] if self.contains_aggregate else []

    @property
    def contains_aggregate(self):
        return False

def test_get_group_by_cols_no_aggregates():
    expr = TestBaseExpression()
    result = expr.get_group_by_cols()
    assert result == [expr]

def test_get_group_by_cols_with_aggregates():
    expr = TestBaseExpression()
    expr.contains_aggregate = True
    result = expr.get_group_by_cols()
    assert len(result) == 2
    assert result[0] == F('username')
    assert result[1] == Value(1)