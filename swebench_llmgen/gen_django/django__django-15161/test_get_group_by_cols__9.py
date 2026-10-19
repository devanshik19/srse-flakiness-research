import pytest
from django.db.models import Expression, F
from django.contrib.auth.models import User

class CustomExpression(Expression):
    def get_source_expressions(self):
        return [F('username'), F('email')]

    @property
    def contains_aggregate(self):
        return False

def test_get_group_by_cols_no_aggregate():
    expr = CustomExpression()
    result = expr.get_group_by_cols()
    assert result == [expr], "Expected group by columns to include the expression itself when no aggregates are present."

def test_get_group_by_cols_with_aggregate():
    class AggregateExpression(Expression):
        def get_source_expressions(self):
            return [CustomExpression(), CustomExpression()]

        @property
        def contains_aggregate(self):
            return True
    
    expr = AggregateExpression()
    result = expr.get_group_by_cols()
    assert len(result) == 2, "Expected group by columns to include all source expressions when aggregates are present."
    assert result[0] is not result[1], "Expected unique expressions to be included in group by columns."