import pytest
from django.db.models import expressions

class TestBaseExpression:
    
    def test_set_source_expressions_empty(self):
        expr = expressions.BaseExpression(output_field=None)
        expr.set_source_expressions([])
        
    def test_set_source_expressions_non_empty(self):
        expr = expressions.BaseExpression(output_field=None)

        with pytest.raises(AssertionError):
            expr.set_source_expressions(['non-empty'])