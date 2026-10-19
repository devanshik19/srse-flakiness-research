import pytest
from django.db.models import F
from django.contrib.auth.models import User
from django.db.models.expressions import BaseExpression

class TestBaseExpression(BaseExpression):
    def get_source_expressions(self):
        return [self]

    def contains_aggregate(self):
        return False

def test_get_group_by_cols_no_aggregate():
    expression = TestBaseExpression(output_field=None)
    result = expression.get_group_by_cols()
    assert result == [expression]

def test_get_group_by_cols_with_aggregate():
    expression = TestBaseExpression(output_field=None)
    
    def contains_aggregate():
        return True
    
    expression.contains_aggregate = contains_aggregate

    # Mock the get_source_expressions method
    def get_source_expressions():
        return [TestBaseExpression(output_field=None)]
    
    expression.get_source_expressions = get_source_expressions
    
    result = expression.get_group_by_cols()
    assert len(result) == 1
    assert result[0] == expression.get_source_expressions()[0]