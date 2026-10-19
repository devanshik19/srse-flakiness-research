import pytest
from django.db.models.expressions import BaseExpression

class TestBaseExpression:
    def test_set_source_expressions(self):
        expression = BaseExpression(output_field=None)
        exprs = []

        # Testing the assertion that should pass when exprs is empty
        expression.set_source_expressions(exprs)

        # Testing the assertion that should fail when exprs is not empty
        exprs = [BaseExpression(output_field=None)]
        
        with pytest.raises(AssertionError):
            expression.set_source_expressions(exprs)