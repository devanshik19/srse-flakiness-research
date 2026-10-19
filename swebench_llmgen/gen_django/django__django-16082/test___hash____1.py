import pytest
from django.contrib.auth.models import User
from django.db.models.expressions import Expression

class TestExpression:
    def test_hash(self):
        user_instance = User(username='testuser', password='password123')
        user_instance.save()

        # Create an instance of Expression with a unique identity based on the user instance
        expression = Expression()
        expression.identity = user_instance.id  # Assuming identity should be set like this

        # Compute hash
        expected_hash = hash(expression.identity)
        assert hash(expression) == expected_hash

        # Test different identity values
        another_expression = Expression()
        another_expression.identity = user_instance.id + 1  # Different identity
        assert hash(expression) != hash(another_expression)

    def test_eq(self):
        user_instance = User(username='testuser', password='password123')
        user_instance.save()

        expression_a = Expression()
        expression_a.identity = user_instance.id

        expression_b = Expression()
        expression_b.identity = user_instance.id

        assert expression_a == expression_b
        assert hash(expression_a) == hash(expression_b)

        expression_c = Expression()
        expression_c.identity = user_instance.id + 1

        assert expression_a != expression_c
        assert hash(expression_a) != hash(expression_c)