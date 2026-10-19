import pytest
from django.contrib.auth.models import User
from django.db.models.expressions import Expression

def test_expression_hash():
    # Create an instance of the Expression class with a mock identity
    expression1 = Expression()
    expression2 = Expression()
    
    # Assuming the identity method sets the identity value to be hashable
    expression1.identity = 1
    expression2.identity = 1
    
    expression3 = Expression()
    expression3.identity = 2

    # Test that two expressions with the same identity hash to the same value
    assert hash(expression1) == hash(expression2)

    # Test that two expressions with different identities hash to different values
    assert hash(expression1) != hash(expression3)

    # Test that the hash remains consistent
    original_hash = hash(expression1)
    assert hash(expression1) == original_hash