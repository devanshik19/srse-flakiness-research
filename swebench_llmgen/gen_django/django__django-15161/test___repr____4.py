import pytest
from django.db.models.expressions import CombinedExpression
from django.contrib.auth.models import User

def test_combined_expression_repr():
    # Create instances to be used as lhs and rhs
    user1 = User(username='user1')
    user2 = User(username='user2')
    
    # Initialize a CombinedExpression
    expr = CombinedExpression(lhs=user1, connector='AND', rhs=user2, output_field=None)
    
    # Check the string representation
    expected_repr = "<CombinedExpression: {}>".format(expr)
    assert repr(expr) == expected_repr