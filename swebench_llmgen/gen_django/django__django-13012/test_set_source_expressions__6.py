import pytest
from django.db.models.expressions import BaseExpression

class TestBaseExpression:

    def test_set_source_expressions_empty(self):
        expr = BaseExpression(output_field=None)
        # Since the function asserts that exprs cannot be non-empty, we call it with an empty list
        expr.set_source_expressions([])
        
        # Verify that the source expressions have not changed (still empty)
        assert expr.get_source_expressions() == []

    def test_set_source_expressions_non_empty(self):
        expr = BaseExpression(output_field=None)
        with pytest.raises(AssertionError):
            expr.set_source_expressions([BaseExpression(output_field=None)])