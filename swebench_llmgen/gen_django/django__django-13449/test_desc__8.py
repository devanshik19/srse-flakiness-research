import pytest
from django.db.models.expressions import OrderBy
from django.contrib.auth.models import User
from django.db.models import F

class TestBaseExpression:
    def test_desc(self):
        # Create a User instance for testing
        user = User.objects.create_user(username='testuser', password='password')

        # Create a BaseExpression instance
        expression = F('username')

        # Call the desc method, which should return an OrderBy instance
        order_by_expression = expression.desc()

        # Verify that the order_by_expression is an instance of OrderBy
        assert isinstance(order_by_expression, OrderBy)

        # Validate the direction of ordering
        assert order_by_expression.descending is True
        
        # Check that the expression is properly set within OrderBy
        assert order_by_expression.source == expression