import pytest
from django.contrib.auth.models import User
from django.db.models import ExpressionWrapper
from django.db.models.expressions import BaseExpression


class TestBaseExpression:
    
    def test_copy(self):
        # Create an instance of BaseExpression
        original_expression = BaseExpression(output_field=User._meta.get_field('username'))
        
        # Use the copy method
        copied_expression = original_expression.copy()
        
        # Assert that the copied expression is a new instance
        assert copied_expression is not original_expression
        
        # Assert that the attributes are equal
        assert copied_expression.output_field == original_expression.output_field