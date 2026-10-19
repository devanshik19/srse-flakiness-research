import pytest
from django.contrib.auth.models import User
from django.db.models import Exists
from django.db.models.query import QuerySet

@pytest.fixture
def user_queryset():
    return User.objects.all()

def test_invert(user_queryset):
    exists_expr = Exists(user_queryset)
    
    # Initially, negated should be False
    assert exists_expr.negated is False
    
    # Invert the expression
    inverted_expr = ~exists_expr
    
    # Check that the original exists expression is unchanged
    assert exists_expr.negated is False
    
    # Check that the inverted expression has negated set to True
    assert inverted_expr.negated is True

    # Verify that both instances are different objects
    assert exists_expr is not inverted_expr

    # Check that the copy method is called correctly
    assert isinstance(inverted_expr, Exists)