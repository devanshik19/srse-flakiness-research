import copy
import datetime
from decimal import Decimal
from django.core.exceptions import EmptyResultSet, FieldError
from django.db.models import Q
from django.db.models.expressions import BaseExpression
from django.contrib.auth.models import User

class TestBaseExpression:

    def test_resolve_expression_no_source_expressions(self):
        expr = BaseExpression("output_field")
        expr.set_source_expressions([])

        resolved = expr.resolve_expression()
        assert resolved.is_summary is False
        assert resolved.get_source_expressions() == []

    def test_resolve_expression_with_source_expressions(self):
        class MockExpression(BaseExpression):
            def __init__(self):
                super().__init__("mock")

            def get_source_expressions(self):
                return [None, None]

            def set_source_expressions(self, exprs):
                pass

            def copy(self):
                return MockExpression()

        expr = MockExpression()
        resolved = expr.resolve_expression()
        assert resolved.is_summary is False
        assert isinstance(resolved, MockExpression)

    def test_resolve_expression_with_summarize(self):
        expr = BaseExpression("output_field")
        expr.set_source_expressions([BaseExpression("inner")])

        resolved = expr.resolve_expression(summarize=True)
        assert resolved.is_summary is True
        assert resolved.get_source_expressions() != []

    def test_resolve_expression_allow_joins(self):
        expr = BaseExpression("output_field")
        expr.set_source_expressions([BaseExpression("inner")])

        resolved = expr.resolve_expression(allow_joins=False)
        assert resolved.get_source_expressions() != []
        assert resolved.is_summary is False