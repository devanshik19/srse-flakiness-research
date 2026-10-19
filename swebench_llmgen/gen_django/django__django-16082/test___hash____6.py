import pytest
from django.contrib.auth.models import User
from django.db.models.expressions import Expression


class TestExpression:
    def test_hash(self):
        # Create an instance of Expression
        expression = Expression()
        
        # Setting the identity directly, simulating the behavior
        expression.identity = 1  # assuming identity is set manually for testing

        # Hash calculation
        hash_value = hash(expression)

        # Verify that the hash is as expected
        assert hash_value == hash(1)
        
    def test_hash_equality(self):
        # Create two instances of Expression with the same identity
        expression1 = Expression()
        expression1.identity = 2  # Simulate the identity

        expression2 = Expression()
        expression2.identity = 2  # Simulate the same identity

        # Test that they have the same hash
        assert hash(expression1) == hash(expression2)

    def test_hash_different_identity(self):
        # Create two instances of Expression with different identities
        expression1 = Expression()
        expression1.identity = 3  # Simulate one identity

        expression2 = Expression()
        expression2.identity = 4  # Simulate a different identity

        # Test that they have different hashes
        assert hash(expression1) != hash(expression2)