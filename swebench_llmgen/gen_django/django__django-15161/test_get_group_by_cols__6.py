import pytest
from django.db.models import F, ExpressionWrapper, Value, IntegerField
from django.contrib.auth.models import User
from django.db.models.expressions import BaseExpression

class TestBaseExpression(BaseExpression):

    def __init__(self, output_field):
        super().__init__(output_field)
        self.contains_aggregate = False

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
    expr = TestBaseExpression(output_field=IntegerField())
    assert expr.get_group_by_cols() == [expr]

def test_get_group_by_cols_with_aggregate():
    expr = TestBaseExpression(output_field=IntegerField())
    expr.contains_aggregate = True
    result = expr.get_group_by_cols()
    assert result == [expr]

def test_get_group_by_cols_nested_expressions():
    inner_expr = TestBaseExpression(output_field=IntegerField())
    outer_expr = TestBaseExpression(output_field=IntegerField())
    outer_expr.contains_aggregate = True
    
    def mocked_get_source_expressions():
        return [inner_expr]

    outer_expr.get_source_expressions = mocked_get_source_expressions
    
    result = outer_expr.get_group_by_cols()
    assert result == [inner_expr]