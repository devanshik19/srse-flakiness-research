import pytest
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.sql.query import Query

def test_split_exclude_nullable_field():
    user_model = User
    query = Query(user_model)
    filter_expr = ('username', 'testuser')
    can_reuse = set()
    
    # Mocking necessary parts of the Query instance for the test
    query.select = [query._get_col('username', query.get_meta())]  # Assuming username is not nullable
    query.is_nullable = lambda field: True  # Pretend username is nullable
    query.add_filter = lambda expr: None  # No-op
    query.clear_ordering = lambda force_empty: None  # No-op
    query.trim_start = lambda path: (path, False)  # No-op

    # Performing the call
    condition, needed_inner = query.split_exclude(filter_expr, can_reuse, ['username'])

    assert condition is not None  # Check if a condition was returned
    assert needed_inner is False  # Validate the expected outcome

def test_split_exclude_not_nullable_field():
    user_model = User
    query = Query(user_model)
    filter_expr = ('email', 'test@example.com')
    can_reuse = set()

    # Mocking necessary parts of the Query instance for the test
    query.select = [query._get_col('email', query.get_meta())]  # Assuming email is not nullable
    query.is_nullable = lambda field: False  # Pretend email is not nullable
    query.add_filter = lambda expr: None  # No-op
    query.clear_ordering = lambda force_empty: None  # No-op
    query.trim_start = lambda path: (path, True)  # Indicating that it contains LOUTER

    # Performing the call
    condition, needed_inner = query.split_exclude(filter_expr, can_reuse, ['email'])

    assert condition is not None  # Check condition was created
    assert needed_inner is False  # Validate the expected outcome

def test_split_exclude_outer_ref():
    user_model = User
    query = Query(user_model)
    filter_expr = ('username', Q(OuterRef('username')))  # Using OuterRef in filter
    can_reuse = set()

    # Mocking necessary parts of the Query instance for the test
    query.select = [query._get_col('username', query.get_meta())]
    query.is_nullable = lambda field: False
    query.add_filter = lambda expr: None
    query.clear_ordering = lambda force_empty: None
    query.trim_start = lambda path: (path, False)

    # Performing the call
    condition, needed_inner = query.split_exclude(filter_expr, can_reuse, ['username'])

    assert condition is not None  # Ensure the condition is created
    assert needed_inner is False  # Validate the expected outcome

def test_split_exclude_using_f_expression():
    user_model = User
    query = Query(user_model)
    filter_expr = ('username', F('username'))  # Using F expression in filter
    can_reuse = set()

    # Mocking necessary parts of the Query instance for the test
    query.select = [query._get_col('username', query.get_meta())]
    query.is_nullable = lambda field: False
    query.add_filter = lambda expr: None
    query.clear_ordering = lambda force_empty: None
    query.trim_start = lambda path: (path, False)

    # Performing the call
    condition, needed_inner = query.split_exclude(filter_expr, can_reuse, ['username'])

    assert condition is not None  # Ensure the condition is created
    assert needed_inner is False  # Validate the expected outcome