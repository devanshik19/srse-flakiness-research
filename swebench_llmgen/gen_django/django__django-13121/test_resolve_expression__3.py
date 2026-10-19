import pytest
from django.contrib.auth.models import User
from django.db.models import Expression
from django.db.models.expressions import BaseExpression


class TestBaseExpression(BaseExpression):
    def __init__(self, output_field=None):
        super().__init__(output_field)
        self.is_summary = False

    def copy(self):
        return TestBaseExpression()

    def get_source_expressions(self):
        return []

    def set_source_expressions(self, exprs):
        self.source_expressions = exprs


def test_resolve_expression_with_default_parameters():
    expr = TestBaseExpression()
    resolved_expr = expr.resolve_expression()
    assert isinstance(resolved_expr, TestBaseExpression)
    assert resolved_expr.is_summary is False


def test_resolve_expression_with_summarize():
    expr = TestBaseExpression()
    resolved_expr = expr.resolve_expression(summarize=True)
    assert isinstance(resolved_expr, TestBaseExpression)
    assert resolved_expr.is_summary is True


def test_resolve_expression_with_source_expressions():
    class TestExpression(BaseExpression):
        def __init__(self, output_field=None):
            super().__init__(output_field)
            self.source_expressions = [TestBaseExpression()]

        def copy(self):
            return TestExpression()

        def get_source_expressions(self):
            return self.source_expressions

    expr = TestExpression()
    resolved_expr = expr.resolve_expression()
    assert isinstance(resolved_expr, TestExpression)
    assert len(resolved_expr.get_source_expressions()) == 1
    assert isinstance(resolved_expr.get_source_expressions()[0], TestBaseExpression)