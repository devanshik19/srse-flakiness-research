import pytest
from django.contrib.auth.models import User
from django.db.models.expressions import CombinedExpression

def test_combined_expression_repr():
    user = User.objects.create(username='testuser')
    
    # Create instances of CombinedExpression for testing
    lhs = user.username
    connector = 'AND'
    rhs = 'other_condition'
    output_field = None  # Assuming None for simplicity as we do not use output_field in __repr__

    # Initialize CombinedExpression instance
    combined_expression = CombinedExpression(lhs, connector, rhs, output_field)

    # Testing __repr__
    expected_repr = "<CombinedExpression: {}>".format(combined_expression)
    actual_repr = repr(combined_expression)

    assert actual_repr == expected_repr, f"Expected: {expected_repr}, but got: {actual_repr}"