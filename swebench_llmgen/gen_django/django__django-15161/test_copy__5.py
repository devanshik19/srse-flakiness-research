import copy
import pytest
from django.contrib.auth.models import User
from django.db.models.expressions import BaseExpression

class TestBaseExpression:

    def test_copy(self):
        # Create an instance of BaseExpression
        expression = BaseExpression(output_field=User._meta.get_field('username'))
        
        # Use the copy method
        copied_expression = expression.copy()
        
        # Ensure that the copied object is a different instance
        assert copied_expression is not expression
        
        # Ensure that the contents of the copied object are equal
        assert copied_expression.output_field == expression.output_field
        
        # Ensure that copying retains all attributes
        assert copied_expression != expression