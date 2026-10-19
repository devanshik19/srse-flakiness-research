import pytest
from django.db.models import Expression

class BaseExpression(Expression):
    def set_source_expressions(self, exprs):
        assert not exprs

# Test Class for BaseExpression
class TestBaseExpression:

    def test_set_source_expressions_empty(self):
        expr = BaseExpression()
        expr.set_source_expressions([])  # Should not raise

    def test_set_source_expressions_non_empty(self):
        expr = BaseExpression()
        with pytest.raises(AssertionError):
            expr.set_source_expressions([1])  # Should raise AssertionError