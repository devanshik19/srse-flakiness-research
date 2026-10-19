import pytest
from django.contrib.auth.models import User
from django.db.models.expressions import BaseExpression

class TestBaseExpression:

    def test_copy_method(self):
        # Arrange
        original_expression = BaseExpression(output_field=None)
        
        # Act
        copied_expression = original_expression.copy()

        # Assert
        assert copied_expression is not original_expression  # Copy should be a different object
        assert isinstance(copied_expression, BaseExpression)  # Copied object should still be an instance of BaseExpression