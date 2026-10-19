import pytest
from django.db.models.sql.query import Query
from django.db.models import Q
from django.contrib.auth.models import User

def test_split_exclude():
    # Setup
    user = User.objects.create(username='testuser', email='test@example.com')
    query = Query(User)

    # Test for known filter expression where the right-hand side is a simple value
    filter_expr = ('username', 'testuser')
    can_reuse = set()
    names_with_path = []

    condition, needed_inner = query.split_exclude(filter_expr, can_reuse, names_with_path)

    # Assert that the condition object was created (not None)
    assert condition is not None
    assert isinstance(condition, Q)

    # Check that the second part of the condition is appropriately filled
    assert needed_inner is False

    # Test when the right-hand side is a F expression
    filter_expr_f = ('email', User.objects.get(id=user.id).email)
    condition_f, needed_inner_f = query.split_exclude(filter_expr_f, can_reuse, names_with_path)

    # Assert return not None for F expression case
    assert condition_f is not None
    assert isinstance(condition_f, Q)

    # Check that the second part of the condition is appropriately filled
    assert needed_inner_f is False

    # Check whether nullable field logic is handled when applicable
    # Update the user to have a nullable field, then test appropriate handling
    user.email = None
    user.save()
    
    filter_expr_nullable = ('email', None)
    condition_nullable, needed_inner_nullable = query.split_exclude(filter_expr_nullable, can_reuse, names_with_path)

    # Assert the condition is not None even when dealing with nullable
    assert condition_nullable is not None
    assert isinstance(condition_nullable, Q)
    assert needed_inner_nullable is False