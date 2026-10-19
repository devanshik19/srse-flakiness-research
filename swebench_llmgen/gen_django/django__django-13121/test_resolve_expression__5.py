import copy
import datetime
import pytest
from decimal import Decimal
from django.core.exceptions import EmptyResultSet, FieldError
from django.db.models import Expression


class TestBaseExpression(Expression):
    def __init__(self, output_field=None):
        super().__init__(output_field=output_field)
        self.is_summary = False

    def get_source_expressions(self):
        return []

    def set_source_expressions(self, exprs):
        pass

    def copy(self):
        return copy.deepcopy(self)

    def resolve_expression(self, query=None, allow_joins=True, reuse=None, summarize=False, for_save=False):
        c = self.copy()
        c.is_summary = summarize
        c.set_source_expressions([
            expr.resolve_expression(query, allow_joins, reuse, summarize)
            if expr else None
            for expr in c.get_source_expressions()
        ])
        return c


@pytest.mark.parametrize("summarize, expected_is_summary", [(True, True), (False, False)])
def test_resolve_expression(summarize, expected_is_summary):
    expression = TestBaseExpression()
    resolved_expression = expression.resolve_expression(summarize=summarize)

    assert resolved_expression.is_summary == expected_is_summary
    assert isinstance(resolved_expression, TestBaseExpression)
    assert resolved_expression.get_source_expressions() == []