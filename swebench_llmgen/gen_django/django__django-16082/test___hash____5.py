import pytest
from django.contrib.auth.models import User
from django.db.models.expressions import Expression

def test_expression_hash():
    user = User.objects.create_user(username='testuser', password='testpass')
    
    expr1 = Expression()
    expr1.identity = user.id  # Assigning identity for hashing
    hash_expr1 = hash(expr1)
    
    expr2 = Expression()
    expr2.identity = user.id  # Same identity so the hash should be identical
    hash_expr2 = hash(expr2)

    assert hash_expr1 == hash_expr2, "Hashes should be equal for expressions with the same identity"

    expr3 = Expression()
    expr3.identity = user.id + 1  # Different identity
    hash_expr3 = hash(expr3)

    assert hash_expr1 != hash_expr3, "Hashes should not be equal for expressions with different identities"