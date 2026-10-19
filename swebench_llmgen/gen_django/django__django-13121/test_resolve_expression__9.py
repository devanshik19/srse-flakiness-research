import pytest
from django.contrib.auth.models import User
from django.db.models import Expression

class TestBaseExpression(Expression):
    def get_source_expressions(self):
        return []

    def copy(self):
        return self.__class__()

@pytest.mark.parametrize("summarize, expected_is_summary", [(False, False), (True, True)])
def test_resolve_expression(summarize, expected_is_summary):
    expression = TestBaseExpression()

    resolved_expression = expression.resolve_expression(summarize=summarize)

    assert isinstance(resolved_expression, TestBaseExpression)
    assert resolved_expression.is_summary == expected_is_summary