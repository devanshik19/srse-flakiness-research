import pytest
from django.contrib.auth.models import User
from django.db.models import F
from django.db.models.expressions import CombinedExpression

def test_combined_expression_repr():
    # Create instances of User model to use as lhs and rhs
    user_1 = User.objects.create(username='user1')
    user_2 = User.objects.create(username='user2')
    
    # Create a CombinedExpression instance
    lhs = F('id')  # Using F expression for lhs
    connector = 'AND'
    rhs = F('username')  # Using F expression for rhs
    output_field = None  # Assuming output_field is None for this example
    
    combined_expression = CombinedExpression(lhs, connector, rhs, output_field)

    # Test __repr__
    expected_repr = f"<CombinedExpression: {combined_expression}>"
    assert repr(combined_expression) == expected_repr