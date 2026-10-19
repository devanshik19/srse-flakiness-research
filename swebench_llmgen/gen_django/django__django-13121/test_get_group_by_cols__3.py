import pytest
from django.db.models import F, Sum
from django.contrib.auth.models import User
from django.db.models.expressions import BaseExpression

class TestBaseExpression(BaseExpression):

    def get_source_expressions(self):
        # Simulating the return of source expressions
        return [F('username'), F('email')]

    @property
    def contains_aggregate(self):
        return False  # Modify this flag to test different paths

def test_get_group_by_cols_no_aggregate():
    expression = TestBaseExpression()
    result = expression.get_group_by_cols()
    assert result == [expression]

def test_get_group_by_cols_with_aggregate():
    expression = TestBaseExpression()
    expression.contains_aggregate = True  # Testing aggregate path
    result = expression.get_group_by_cols()
    assert len(result) == 2  # Expecting 2 source expressions
    assert result[0] == F('username')
    assert result[1] == F('email')