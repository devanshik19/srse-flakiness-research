import pytest
from django.contrib.auth.models import User
from django.db.models.expressions import Expression

class TestExpression:

    def test_hash(self):
        user = User.objects.create(username='testuser', password='password123')
        expression = Expression()
        expression.identity = user.pk  # Assigning an example identity to the expression

        # Check that the hash of the expression is equal to the hash of its identity
        assert hash(expression) == hash(expression.identity)

    def test_hash_unique_for_different_identities(self):
        expression1 = Expression()
        expression1.identity = 1
        
        expression2 = Expression()
        expression2.identity = 2
        
        # Ensure hashes are different for different identities
        assert hash(expression1) != hash(expression2)