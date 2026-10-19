import pytest
from django.contrib.auth.models import User
from django.db.models import Exists

@pytest.fixture
def user_queryset():
    return User.objects.all()

def test_invert_exists(user_queryset):
    exists_expr = Exists(user_queryset)
    
    # Check initial negated state
    assert exists_expr.negated is False
    
    # Invert the Exists expression
    inverted_exists_expr = ~exists_expr
    
    # Check the negated state of the inverted expression
    assert inverted_exists_expr.negated is True
    assert inverted_exists_expr.template == exists_expr.template
    assert inverted_exists_expr.output_field == exists_expr.output_field

    # Verify that the original is not modified
    assert exists_expr.negated is False