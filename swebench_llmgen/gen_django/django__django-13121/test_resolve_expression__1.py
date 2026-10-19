import copy
import datetime
from decimal import Decimal
import pytest
from django.core.exceptions import EmptyResultSet, FieldError
from django.db import NotSupportedError, connection
from django.db.models import F
from django.db.models.expressions import BaseExpression
from django.contrib.auth.models import User

class TestBaseExpression(BaseExpression):
    def __init__(self, output_field):
        super().__init__(output_field)
        self.is_summary = False

    def get_source_expressions(self):
        return []

    def set_source_expressions(self, exprs):
        self.source_expressions = exprs

    def copy(self):
        return copy.deepcopy(self)

def test_resolve_expression_no_query():
    expression = TestBaseExpression(output_field=None)
    resolved_expression = expression.resolve_expression()
    
    assert resolved_expression is not None
    assert isinstance(resolved_expression, TestBaseExpression)
    assert resolved_expression.is_summary is False

def test_resolve_expression_with_summarize():
    expression = TestBaseExpression(output_field=None)
    resolved_expression = expression.resolve_expression(summarize=True)
    
    assert resolved_expression.is_summary is True

def test_resolve_expression_with_source_expressions():
    expression = TestBaseExpression(output_field=None)
    expression.set_source_expressions([TestBaseExpression(output_field=None)])
    resolved_expression = expression.resolve_expression()
    
    assert len(resolved_expression.get_source_expressions()) == 1
    assert resolved_expression.get_source_expressions()[0] is not None

def test_resolve_expression_with_allow_joins():
    expression = TestBaseExpression(output_field=None)
    resolved_expression = expression.resolve_expression(allow_joins=False)
    
    assert not resolved_expression.is_summary  # Not affected by allow_joins

def test_copy_functionality():
    expression = TestBaseExpression(output_field=None)
    resolved_expression = expression.resolve_expression()
    
    assert expression is not resolved_expression  # Ensure distinct objects
    assert expression.copy() is not expression  # Ensure copy is distinct