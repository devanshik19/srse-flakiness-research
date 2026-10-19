import pytest
from django.db.models import Func
from django.contrib.auth.models import User
from django.db import models
from django.db.models.expressions import BaseExpression

class TestBaseExpression(BaseExpression):

    def __init__(self, output_field=None):
        super().__init__(output_field)

    def copy(self):
        return TestBaseExpression()

    def get_source_expressions(self):
        return []

    def set_source_expressions(self, exprs):
        self.source_expressions = exprs

class SimpleExpression(TestBaseExpression):

    def copy(self):
        return SimpleExpression()

class TestResolveExpression:

    def test_resolve_expression_no_query(self):
        expr = SimpleExpression()
        resolved = expr.resolve_expression()
        assert resolved.is_summary is False
        assert isinstance(resolved, SimpleExpression)

    def test_resolve_expression_with_summarize(self):
        expr = SimpleExpression()
        resolved = expr.resolve_expression(summarize=True)
        assert resolved.is_summary is True

    def test_resolve_expression_with_source_expressions(self):
        expr = SimpleExpression()
        expr.set_source_expressions([SimpleExpression(), SimpleExpression()])
        resolved = expr.resolve_expression()
        assert resolved.get_source_expressions() == [SimpleExpression(), SimpleExpression()]

    def test_resolve_expression_with_allow_joins(self):
        expr = SimpleExpression()
        resolved = expr.resolve_expression(allow_joins=False)
        assert resolved.is_summary is False
        assert isinstance(resolved, SimpleExpression)

    def test_resolve_expression_with_reuse(self):
        expr = SimpleExpression()
        reuse_set = set()
        resolved = expr.resolve_expression(reuse=reuse_set)
        assert resolved.is_summary is False
        assert isinstance(resolved, SimpleExpression)