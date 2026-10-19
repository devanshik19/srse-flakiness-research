import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import Query
from django.db.models import Q, OuterRef, F

@pytest.fixture
def setup_query():
    user_model = User
    query = Query(user_model)
    return query

def test_split_exclude_with_outerref(setup_query):
    query = setup_query
    filter_expr = ('username', OuterRef('username'))
    can_reuse = set()
    names_with_path = ['username']

    condition, needed_inner = query.split_exclude(filter_expr, can_reuse, names_with_path)

    assert condition is not None
    assert needed_inner is False

def test_split_exclude_with_f_expression(setup_query):
    query = setup_query
    filter_expr = ('username', F('username'))
    can_reuse = set()
    names_with_path = ['username']

    condition, needed_inner = query.split_exclude(filter_expr, can_reuse, names_with_path)

    assert condition is not None
    assert needed_inner is False

def test_split_exclude_with_nullable_field(setup_query):
    user_model = User
    query = Query(user_model)
    user_model._meta.get_field('email').null = True  # Simulate a nullable field

    filter_expr = ('email', 'test@example.com')
    can_reuse = set()
    names_with_path = ['email']

    condition, needed_inner = query.split_exclude(filter_expr, can_reuse, names_with_path)

    assert condition is not None
    assert needed_inner is False

def test_split_exclude_in_with_conditions(setup_query):
    user_model = User
    query = Query(user_model)

    filter_expr = ('username', 'admin')
    can_reuse = {query.get_initial_alias()}  # Simulate a reusable alias
    names_with_path = ['username']

    condition, needed_inner = query.split_exclude(filter_expr, can_reuse, names_with_path)

    assert condition is not None
    assert needed_inner is False