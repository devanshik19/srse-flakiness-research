import pytest
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.sql.query import Query

@pytest.fixture
def setup_query():
    user_model = User
    return Query(user_model)

def test_split_exclude_no_f_filter(setup_query):
    query = setup_query
    filter_expr = ('username', 'testuser')
    can_reuse = set()
    names_with_path = ['username']
    
    condition, needed_inner = query.split_exclude(filter_expr, can_reuse, names_with_path)
    
    assert condition is not None
    assert needed_inner is False

def test_split_exclude_with_f_filter(setup_query):
    query = setup_query
    filter_expr = ('username', F('email'))
    can_reuse = set()
    names_with_path = ['username']

    condition, needed_inner = query.split_exclude(filter_expr, can_reuse, names_with_path)

    assert condition is not None
    assert needed_inner is False

def test_split_exclude_nullable_field(setup_query):
    query = setup_query
    filter_expr = ('last_login', None)  # Last login is nullable for User
    can_reuse = set()
    names_with_path = ['last_login']

    condition, needed_inner = query.split_exclude(filter_expr, can_reuse, names_with_path)

    assert condition is not None
    assert needed_inner is False

def test_split_exclude_with_reuse(setup_query):
    query = setup_query
    filter_expr = ('username', 'testuser')
    can_reuse = {'auth_user'}
    names_with_path = ['username']
    
    condition, needed_inner = query.split_exclude(filter_expr, can_reuse, names_with_path)

    assert condition is not None
    assert needed_inner is False

def test_split_exclude_with_louter(setup_query):
    query = setup_query
    filter_expr = ('email', 'example@test.com')
    can_reuse = {'auth_user'}
    names_with_path = ['email']

    condition, needed_inner = query.split_exclude(filter_expr, can_reuse, names_with_path)

    # This test is designed to check if the condition is created correctly
    assert condition is not None
    assert needed_inner is False