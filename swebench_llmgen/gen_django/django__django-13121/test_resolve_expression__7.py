import copy
import datetime
from decimal import Decimal
from django.core.exceptions import EmptyResultSet, FieldError
from django.db import NotSupportedError, connection
from django.db.models import F
from django.db.models.expressions import BaseExpression
from django.utils.functional import cached_property

class TestBaseExpression(BaseExpression):
    def __init__(self, output_field=None):
        super().__init__(output_field)
        self.is_summary = False

    def get_source_expressions(self):
        return []

    def set_source_expressions(self, exprs):
        pass

    def copy(self):
        return copy.deepcopy(self)

def test_resolve_expression_no_joins():
    expr = TestBaseExpression()
    resolved = expr.resolve_expression(query=None, allow_joins=False, reuse=None, summarize=False, for_save=False)
    
    assert resolved.is_summary is False
    assert isinstance(resolved, TestBaseExpression)

def test_resolve_expression_with_summarize():
    expr = TestBaseExpression()
    resolved = expr.resolve_expression(query=None, allow_joins=True, reuse=None, summarize=True, for_save=False)
    
    assert resolved.is_summary is True
    assert isinstance(resolved, TestBaseExpression)

def test_resolve_expression_with_source_expressions():
    class TestExpression(TestBaseExpression):
        def get_source_expressions(self):
            return [TestBaseExpression()]

    expr = TestExpression()
    resolved = expr.resolve_expression(query=None, allow_joins=True, reuse=None, summarize=False, for_save=False)
    
    assert resolved.is_summary is False
    assert len(resolved.get_source_expressions()) == 1
    assert isinstance(resolved.get_source_expressions()[0], TestBaseExpression)