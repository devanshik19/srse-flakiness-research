import pytest
from django.db.models import expressions

class TestBaseExpression:
    
    def test_set_source_expressions_empty(self):
        expr = expressions.BaseExpression(output_field=None)
        result = expr.set_source_expressions([])
        assert result is None  # since the assert in the function doesn't raise an error

    def test_set_source_expressions_non_empty(self):
        expr = expressions.BaseExpression(output_field=None)
        with pytest.raises(AssertionError):
            expr.set_source_expressions([expressions.F('username')])