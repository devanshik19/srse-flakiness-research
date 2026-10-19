import pytest
from django.db.models import Expression
from django.db.models.expressions import BaseExpression

class TestBaseExpression:

    def test_set_source_expressions_empty(self):
        expr = BaseExpression(output_field=None)
        expr.set_source_expressions([])  # Test with empty list
        assert expr.get_source_expressions() == []

    def test_set_source_expressions_non_empty_assertion(self):
        expr = BaseExpression(output_field=None)
        with pytest.raises(AssertionError):
            expr.set_source_expressions([Expression()])  # Test with non-empty list