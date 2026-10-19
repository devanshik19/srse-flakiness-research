import pytest
from django.contrib.auth.models import User
from django.db.models.expressions import Expression

class TestExpression:
    def test_hash(self):
        user = User.objects.create(username='testuser', password='testpass')
        expression1 = Expression()
        expression2 = Expression()

        # Since the expression doesn't have fields affecting identity, we simulate an identity
        expression1.identity = (user.pk, 'some_unique_identifier')
        expression2.identity = (user.pk, 'some_unique_identifier')

        # Hash should be consistent for the same identity
        assert hash(expression1) == hash(expression2)

        # Change identity to ensure different hash
        expression2.identity = (user.pk, 'another_unique_identifier')
        assert hash(expression1) != hash(expression2)

        # Test with a different user to ensure the hash remains unique
        user2 = User.objects.create(username='testuser2', password='testpass2')
        expression3 = Expression()
        expression3.identity = (user2.pk, 'some_unique_identifier')

        assert hash(expression1) != hash(expression3)