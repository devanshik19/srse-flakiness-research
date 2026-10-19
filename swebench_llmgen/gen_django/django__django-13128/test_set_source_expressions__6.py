import pytest
from django.db.models.expressions import BaseExpression

class TestBaseExpression:

    def test_set_source_expressions_empty(self):
        # Create an instance of BaseExpression
        expression = BaseExpression(output_field=None)
        
        # Call the set_source_expressions method with an empty list
        expression.set_source_expressions([])

        # Since assert not exprs is called, there should be no exception raised.

    def test_set_source_expressions_non_empty(self):
        # Create an instance of BaseExpression
        expression = BaseExpression(output_field=None)

        # Check that calling set_source_expressions with non-empty list raises an AssertionError
        with pytest.raises(AssertionError):
            expression.set_source_expressions([1, 2, 3])