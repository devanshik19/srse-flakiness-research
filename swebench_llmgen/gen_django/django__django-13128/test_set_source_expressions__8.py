import pytest
from django.db.models.expressions import BaseExpression

class TestBaseExpression:

    def test_set_source_expressions_empty(self):
        base_expr = BaseExpression(output_field=None)
        result = base_expr.set_source_expressions([])
        assert result is None

    def test_set_source_expressions_non_empty_raises_assertion_error(self):
        base_expr = BaseExpression(output_field=None)
        with pytest.raises(AssertionError):
            base_expr.set_source_expressions([1])