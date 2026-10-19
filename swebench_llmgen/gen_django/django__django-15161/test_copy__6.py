import pytest
import copy
from django.contrib.auth.models import User
from django.db.models.expressions import BaseExpression

class TestBaseExpression:
    
    class TestExpression(BaseExpression):
        def __init__(self, output_field=None):
            super().__init__(output_field)
            self.field_name = "test_field"

    def test_copy(self):
        original_expression = self.TestExpression(output_field="some_field")
        copied_expression = original_expression.copy()

        assert copied_expression is not original_expression  # Check that it's a different instance
        assert copied_expression.field_name == original_expression.field_name  # Check attribute equality
        assert copied_expression.output_field == original_expression.output_field  # Check output field