import pytest
from django.db.models import Q
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

@pytest.fixture
def user_queryset():
    return User.objects.all()

def test_split_exclude_with_simple_filter(user_queryset):
    query = Query(User)
    filter_expr = ('username', 'testuser')
    can_reuse = set()
    names_with_path = []

    condition, needed_inner = query.split_exclude(filter_expr, can_reuse, names_with_path)

    assert condition is not None
    assert needed_inner is False

def test_split_exclude_with_nullable_field(user_queryset):
    # Create a user with a nullable field (if any) to test against, adjust if needed
    user = User.objects.create(username='testuser', email=None)

    query = Query(User)
    filter_expr = ('email', None)
    can_reuse = set()
    names_with_path = []

    condition, needed_inner = query.split_exclude(filter_expr, can_reuse, names_with_path)

    assert condition is not None
    assert needed_inner is False

def test_split_exclude_with_foreign_key(user_queryset):
    # Example of a foreign key related field (assuming User model has a foreign key)
    filter_expr = ('profile__bio', 'test bio')  # Adjust to the actual User model relation if needed
    can_reuse = set()
    names_with_path = ['profile']

    query = Query(User)
    condition, needed_inner = query.split_exclude(filter_expr, can_reuse, names_with_path)

    assert condition is not None
    assert needed_inner is True

def test_split_exclude_with_F_expression(user_queryset):
    from django.db.models import F

    query = Query(User)
    filter_expr = ('email', F('username'))  # Assuming the email should not equal username
    can_reuse = set()
    names_with_path = []

    condition, needed_inner = query.split_exclude(filter_expr, can_reuse, names_with_path)

    assert condition is not None
    assert needed_inner is False