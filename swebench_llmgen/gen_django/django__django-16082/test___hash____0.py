import pytest
from django.contrib.auth.models import User
from django.db.models.expressions import Expression

class TestExpression:
    def test_hash(self):
        user = User.objects.create(username='testuser')
        expr1 = Expression()
        expr1.identity = user.pk  # Using user primary key as identity

        expr2 = Expression()
        expr2.identity = user.pk  # Same identity as expr1

        expr3 = Expression()
        expr3.identity = 'different_identity'  # Different identity

        assert hash(expr1) == hash(expr2)  # Same identity should have same hash
        assert hash(expr1) != hash(expr3)  # Different identity should have different hash