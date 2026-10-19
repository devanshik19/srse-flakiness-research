import pytest
from django.db.models import OuterRef, Subquery, Count
from django.contrib.auth.models import User
from django.db.models.expressions import BaseExpression

class CustomExpression(BaseExpression):
    def __init__(self, output_field=None):
        super().__init__(output_field)
        self.sources = []

    def get_source_expressions(self):
        return self.sources

    def contains_aggregate(self):
        return False

def test_get_group_by_cols_no_aggregate():
    expression = CustomExpression()
    result = expression.get_group_by_cols()
    assert result == [expression]

def test_get_group_by_cols_with_aggregate():
    expression = CustomExpression()
    inner_expression = CustomExpression()
    inner_expression.sources.append(expression)
    
    expression.sources.append(inner_expression)
    
    # Scenario with aggregates
    def mock_contains_aggregate():
        return True
    
    original_contains_aggregate = inner_expression.contains_aggregate
    inner_expression.contains_aggregate = mock_contains_aggregate
    
    result = inner_expression.get_group_by_cols()
    
    # Ensure it collects group by columns
    assert expression in result
    assert inner_expression in result
    
    # Restore original function
    inner_expression.contains_aggregate = original_contains_aggregate