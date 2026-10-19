import pytest
from django.contrib.auth.models import User
from django.db.models.expressions import Expression

class TestExpression:

    def test_hash_identity(self):
        user = User.objects.create_user(username='testuser', password='password')
        
        expression1 = Expression()
        expression1.identity = user.pk
        hash1 = hash(expression1)

        expression2 = Expression()
        expression2.identity = user.pk
        hash2 = hash(expression2)

        assert hash1 == hash2

    def test_hash_different_identity(self):
        user1 = User.objects.create_user(username='user1', password='password1')
        user2 = User.objects.create_user(username='user2', password='password2')
        
        expression1 = Expression()
        expression1.identity = user1.pk
        hash1 = hash(expression1)

        expression2 = Expression()
        expression2.identity = user2.pk
        hash2 = hash(expression2)

        assert hash1 != hash2