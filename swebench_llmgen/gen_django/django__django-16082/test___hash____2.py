import pytest
from django.contrib.auth.models import User
from django.db.models.expressions import Expression


class TestExpression:
    def setup_method(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.expression = Expression()
        self.expression.identity = self.user.id  # Set up an identity for the hash function

    def test_hash(self):
        # Test that the hash function returns the correct hash value based on the identity
        expected_hash = hash(self.user.id)
        assert hash(self.expression) == expected_hash

    def test_hash_equality(self):
        # Test that two expressions with the same identity hash to the same value
        expression2 = Expression()
        expression2.identity = self.user.id
        
        assert hash(self.expression) == hash(expression2)
        assert self.expression.__eq__(expression2)  # Ensure they are considered equal