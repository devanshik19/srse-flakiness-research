import pytest
from django.db.models.expressions import BaseExpression

class TestBaseExpression:

    def test_set_source_expressions_empty(self):
        expr = BaseExpression(output_field=None)
        expr.set_source_expressions([])  # Should pass without assertion
        
    def test_set_source_expressions_non_empty(self):
        expr = BaseExpression(output_field=None)
        
        with pytest.raises(AssertionError):
            expr.set_source_expressions([1, 2, 3])  # Should raise AssertionError