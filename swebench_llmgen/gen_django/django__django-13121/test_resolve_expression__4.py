import pytest
from django.db.models.expressions import BaseExpression
from django.db.models import Value
from django.contrib.auth.models import User


class TestBaseExpression(BaseExpression):
    def __init__(self, output_field):
        super().__init__(output_field)
        self._source_expressions = []

    def get_source_expressions(self):
        return self._source_expressions

    def set_source_expressions(self, exprs):
        self._source_expressions = exprs

    def copy(self):
        return TestBaseExpression(self.output_field)


def test_resolve_expression_no_source_expressions():
    expr = TestBaseExpression(output_field=Value('test'))
    resolved_expr = expr.resolve_expression()

    assert isinstance(resolved_expr, TestBaseExpression)
    assert resolved_expr.is_summary is False
    assert resolved_expr.get_source_expressions() == []


def test_resolve_expression_with_source_expressions():
    expr = TestBaseExpression(output_field=Value('test'))
    expr.set_source_expressions([Value('source1'), Value('source2')])
    resolved_expr = expr.resolve_expression()

    assert isinstance(resolved_expr, TestBaseExpression)
    assert resolved_expr.is_summary is False
    assert len(resolved_expr.get_source_expressions()) == 2


def test_resolve_expression_summary():
    expr = TestBaseExpression(output_field=Value('test'))
    resolved_expr = expr.resolve_expression(summarize=True)

    assert isinstance(resolved_expr, TestBaseExpression)
    assert resolved_expr.is_summary is True


def test_resolve_expression_with_allow_joins():
    expr = TestBaseExpression(output_field=Value('test'))
    expr.set_source_expressions([Value('source1')])
    resolved_expr = expr.resolve_expression(allow_joins=False)

    assert isinstance(resolved_expr, TestBaseExpression)
    assert resolved_expr.get_source_expressions()[0] is not None