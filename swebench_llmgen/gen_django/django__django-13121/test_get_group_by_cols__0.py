import pytest
from django.db.models import Expression, F
from django.contrib.auth.models import User

class BaseExpression(Expression):
    def __init__(self, output_field=None):
        self.output_field = output_field

    @property
    def contains_aggregate(self):
        return False

    def get_source_expressions(self):
        return [self]

    def get_group_by_cols(self, alias=None):
        if not self.contains_aggregate:
            return [self]
        cols = []
        for source in self.get_source_expressions():
            cols.extend(source.get_group_by_cols())
        return cols

def test_get_group_by_cols_no_aggregate():
    expr = BaseExpression()
    result = expr.get_group_by_cols()
    assert result == [expr]

def test_get_group_by_cols_with_source_expressions():
    class TestExpression(BaseExpression):
        def __init__(self, *expressions):
            super().__init__()
            self.source_expressions = expressions
        
        def get_source_expressions(self):
            return self.source_expressions

    expr1 = TestExpression()
    expr2 = TestExpression()
    combined_expr = TestExpression(expr1, expr2)

    result = combined_expr.get_group_by_cols()
    assert result == [expr1, expr2]

def test_get_group_by_cols_with_aggregate():
    class AggregateExpression(BaseExpression):
        @property
        def contains_aggregate(self):
            return True

    expr = AggregateExpression()
    result = expr.get_group_by_cols()
    assert result == [expr]