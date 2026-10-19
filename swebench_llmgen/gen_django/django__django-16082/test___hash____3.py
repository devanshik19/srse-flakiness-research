import pytest
from django.contrib.auth.models import User
from django.db.models.expressions import Expression

@pytest.mark.parametrize("identity_value", [1, "test", (1, 2, 3)])
def test_expression_hash(identity_value):
    # Create a subclass for testing purposes
    class TestExpression(Expression):
        def __init__(self, identity):
            self.identity = identity

    expr = TestExpression(identity_value)
    
    # Ensure that the hash is consistent
    hash_value = hash(expr)
    assert hash_value == hash(expr)

    # Different identities should produce different hashes
    if isinstance(identity_value, (int, str, tuple)):
        different_expr = TestExpression(identity_value + "1" if isinstance(identity_value, str) else identity_value + 1)
        assert hash(expr) != hash(different_expr)

    # Testing identity consistency
    assert expr.__hash__() == hash(expr.identity)