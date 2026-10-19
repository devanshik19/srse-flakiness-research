import pytest
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.sql.query import Query

@pytest.fixture
def user_queryset():
    # Create some users for testing
    User.objects.create(username='user1', email='user1@example.com')
    User.objects.create(username='user2', email='user2@example.com')
    User.objects.create(username='user3', email='user3@example.com')
    return User.objects.all()

def test_split_exclude_with_outerref(user_queryset):
    query = Query(User)  
    filter_expr = ('username', Q(username='user1'))
    can_reuse = set()
    names_with_path = []

    condition, needed_inner = query.split_exclude(filter_expr, can_reuse, names_with_path)

    # Should generate a condition for outer username not in the subquery
    assert condition is not None
    assert 'NOT IN' in str(condition) or 'IS NOT NULL' in str(condition)
    assert needed_inner is False

def test_split_exclude_with_f(user_queryset):
    query = Query(User)  
    filter_expr = ('email', F('email'))
    can_reuse = set([User._meta.pk])
    names_with_path = []

    condition, needed_inner = query.split_exclude(filter_expr, can_reuse, names_with_path)

    # Validate the generated condition
    assert condition is not None
    assert 'NOT IN' in str(condition)
    assert needed_inner is False

def test_split_exclude_with_null(user_queryset):
    query = Query(User)
    filter_expr = ('username', 'user2')
    can_reuse = set()
    names_with_path = []

    condition, needed_inner = query.split_exclude(filter_expr, can_reuse, names_with_path)

    # Ensure it adds necessary null checks
    assert condition is not None
    assert 'IS NOT NULL' in str(condition)
    assert needed_inner is False