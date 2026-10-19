import pytest
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.sql.query import Query

@pytest.fixture
def query_instance():
    # Create a queryset and initialize a Query instance
    user_qs = User.objects.all()
    return Query(User, user_qs.query.where)

def test_split_exclude_basic(query_instance):
    filter_expr = ('username', 'testuser')
    can_reuse = set()
    names_with_path = []

    condition, needed_inner = query_instance.split_exclude(filter_expr, can_reuse, names_with_path)

    assert condition is not None
    assert isinstance(condition, Q)

def test_split_exclude_with_nullable_field(query_instance):
    filter_expr = ('email', 'test@example.com')
    can_reuse = set()
    names_with_path = []

    # Add a test user with a nullable field
    User.objects.create(username='testuser', email='test@example.com')

    condition, needed_inner = query_instance.split_exclude(filter_expr, can_reuse, names_with_path)

    assert condition is not None
    assert hasattr(condition, 'children')
    
    # Check if nullable condition is incorporated
    assert any('isnull' in str(cond) for cond in condition.children)

def test_split_exclude_with_outerref(query_instance):
    filter_expr = ('username', User.objects.create(username='outerref_test').pk)
    can_reuse = set()
    names_with_path = []

    condition, needed_inner = query_instance.split_exclude(filter_expr, can_reuse, names_with_path)

    assert condition is not None
    assert isinstance(condition, Q)
    assert 'NOT IN' in str(condition)

def test_split_exclude_with_complex_filter(query_instance):
    filter_expr = ('profile__bio', 'example')  # Assuming User has a OneToOneField with a Profile model
    can_reuse = {'user'}
    names_with_path = ['profile']

    condition, needed_inner = query_instance.split_exclude(filter_expr, can_reuse, names_with_path)

    assert condition is not None
    assert isinstance(condition, Q)
    assert len(condition.children) > 0

def test_split_exclude_with_empty_filter(query_instance):
    filter_expr = ()
    can_reuse = set()
    names_with_path = []

    with pytest.raises(ValueError):
        query_instance.split_exclude(filter_expr, can_reuse, names_with_path)