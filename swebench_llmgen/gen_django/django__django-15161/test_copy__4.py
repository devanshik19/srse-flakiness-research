import copy
import pytest
from django.db.models.expressions import BaseExpression
from django.contrib.auth.models import User

class TestBaseExpression:

    def test_copy_method(self):
        # Given
        expression = BaseExpression(output_field=None)

        # When
        copied_expression = expression.copy()

        # Then
        assert copied_expression is not expression  # Ensure it is a different object
        assert isinstance(copied_expression, BaseExpression)  # Ensure the copied object is of the same type