import pytest
from django.db.models.expressions import BaseExpression

class TestBaseExpression:

    def test_set_source_expressions_empty(self):
        expression = BaseExpression(output_field=None)
        expression.set_source_expressions([])  # No assertion error should be raised

    def test_set_source_expressions_non_empty(self):
        expression = BaseExpression(output_field=None)
        with pytest.raises(AssertionError):
            expression.set_source_expressions([BaseExpression(output_field=None)])