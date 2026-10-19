import pytest
from django.db.models import Expression
from django.contrib.auth.models import User

class TestBaseExpression(Expression):

    def contains_aggregate(self):
        return False

    def get_source_expressions(self):
        return []

def test_get_group_by_cols_no_aggregate():
    expr = TestBaseExpression()
    result = expr.get_group_by_cols()
    assert result == [expr]


class TestBaseExpressionWithAggregate(TestBaseExpression):

    def contains_aggregate(self):
        return True

    def get_source_expressions(self):
        return [TestBaseExpression()]


def test_get_group_by_cols_with_aggregate():
    expr = TestBaseExpressionWithAggregate()
    result = expr.get_group_by_cols()
    assert len(result) == 1
    assert isinstance(result[0], TestBaseExpression)