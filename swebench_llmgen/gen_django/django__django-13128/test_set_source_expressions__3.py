import pytest
from django.db.models.expressions import BaseExpression

class TestBaseExpression:

    def test_set_source_expressions_with_empty_exprs(self):
        expression = BaseExpression(output_field=None)
        expression.set_source_expressions([])

    def test_set_source_expressions_with_non_empty_exprs(self):
        expression = BaseExpression(output_field=None)

        with pytest.raises(AssertionError):
            expression.set_source_expressions(['not_empty'])