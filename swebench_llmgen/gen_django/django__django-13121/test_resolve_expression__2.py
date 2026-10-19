import pytest
from django.db.models import Expression
from django.contrib.auth.models import User

class TestBaseExpression(Expression):

    def __init__(self, output_field=None):
        super().__init__(output_field=output_field)

    def get_source_expressions(self):
        return []

    def set_source_expressions(self, exprs):
        pass

    def copy(self):
        return TestBaseExpression(self.output_field)

def test_resolve_expression_no_query():
    expr = TestBaseExpression()
    result = expr.resolve_expression()
    assert isinstance(result, TestBaseExpression)
    assert result.is_summary is False

def test_resolve_expression_with_summary():
    expr = TestBaseExpression()
    result = expr.resolve_expression(summarize=True)
    assert result.is_summary is True

def test_resolve_expression_with_source_expressions():
    class InnerExpression(TestBaseExpression):
        def get_source_expressions(self):
            return [TestBaseExpression()]

    expr = InnerExpression()
    result = expr.resolve_expression()
    assert isinstance(result, InnerExpression)
    assert len(result.get_source_expressions()) == 1

def test_resolve_expression_with_allow_joins():
    expr = TestBaseExpression()
    result = expr.resolve_expression(allow_joins=True)
    assert isinstance(result, TestBaseExpression)

def test_resolve_expression_with_reuse():
    expr = TestBaseExpression()
    result = expr.resolve_expression(reuse=set())
    assert isinstance(result, TestBaseExpression)