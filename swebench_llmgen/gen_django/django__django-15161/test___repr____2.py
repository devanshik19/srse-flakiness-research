import pytest
from django.contrib.auth.models import User
from django.db.models import expressions

def test_combined_expression_repr():
    # Creating an instance of CombinedExpression
    lhs = expressions.F('username')  # Using existing User model fields
    connector = 'AND'
    rhs = expressions.F('email')
    output_field = expressions.IntegerField()

    combined_expression = expressions.CombinedExpression(lhs, connector, rhs, output_field)

    # Expected representation
    expected_repr = "<CombinedExpression: F('username') AND F('email')>"
    
    # Check the __repr__ method
    assert repr(combined_expression) == expected_repr