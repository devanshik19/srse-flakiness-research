import pytest
from django.db.models import Q
from django.contrib.auth.models import User
from django.db.models.sql.query import Query


def test_split_exclude():
    user = User.objects.create(username='testuser', email='test@example.com')
    filter_expr = ('is_staff', False)
    can_reuse = set()
    names_with_path = ['user']

    query = Query(User)

    # Test with a regular filter
    condition, needed_inner = query.split_exclude(filter_expr, can_reuse, names_with_path)
    assert condition is not None
    assert 'NOT IN' in str(condition)

    # Test with a subquery (using OuterRef)
    filter_expr = ('is_active', Q(user__username='testuser'))
    condition, needed_inner = query.split_exclude(filter_expr, can_reuse, names_with_path)
    assert condition is not None
    assert 'NOT IN' in str(condition)

    # Test with nullable field scenario
    user.is_active = None
    user.save()
    filter_expr = ('is_active', None)
    condition, needed_inner = query.split_exclude(filter_expr, can_reuse, names_with_path)
    assert condition is not None
    assert 'IS NULL' in str(condition)

    # Test the contains_louter condition
    contains_louter_case = ('username', 'testuser')
    condition, needed_inner = query.split_exclude(contains_louter_case, can_reuse, names_with_path)
    assert condition is not None
    assert 'IS NOT NULL' in str(condition)