import pytest
from django.db.models import Expression, Value
from django.contrib.auth.models import User

class BaseExpression(Expression):
    def set_source_expressions(self, exprs):
        assert not exprs

# Test class for BaseExpression
class TestBaseExpression:
    def test_set_source_expressions_empty(self):
        expr = BaseExpression(output_field=Value("Test"))
        expr.set_source_expressions([])  # This should not raise an assertion error

    def test_set_source_expressions_non_empty(self):
        expr = BaseExpression(output_field=Value("Test"))
        with pytest.raises(AssertionError):
            expr.set_source_expressions([Value("Not Empty")])