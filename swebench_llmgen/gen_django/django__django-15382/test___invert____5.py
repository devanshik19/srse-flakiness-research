import pytest
from django.contrib.auth.models import User
from django.db.models import Exists

@pytest.mark.django_db
def test_invert():
    # Create a sample user
    User.objects.create(username='testuser1', password='password123')
    
    # Create an Exists expression based on the User model
    exists_expr = Exists(User.objects.filter(username='testuser1'))

    # Check the initial state
    assert not exists_expr.negated

    # Invert the expression
    inverted_expr = ~exists_expr

    # Check the inverted state
    assert inverted_expr.negated
    assert inverted_expr.template == exists_expr.template
    assert inverted_expr.output_field == exists_expr.output_field