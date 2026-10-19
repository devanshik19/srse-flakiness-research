import pytest
from django.db.models import Expression
from django.contrib.auth.models import User


class TestBaseExpression(Expression):

    def contains_aggregate(self):
        return False

    def get_source_expressions(self):
        return []


def test_get_group_by_cols_no_aggregate():
    expression = TestBaseExpression()
    result = expression.get_group_by_cols()
    assert result == [expression]


def test_get_group_by_cols_with_aggregate():
    class MockSourceExpression(TestBaseExpression):
        def contains_aggregate(self):
            return True

        def get_source_expressions(self):
            return [TestBaseExpression(), TestBaseExpression()]

    expression = MockSourceExpression()
    result = expression.get_group_by_cols()
    assert len(result) == 2
    assert expression.get_source_expressions() == result[0:2]