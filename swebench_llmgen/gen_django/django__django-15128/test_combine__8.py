import pytest
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.sql.query import Query

@pytest.fixture
def user_query():
    return Query(User)

@pytest.fixture
def another_user_query():
    return Query(User)

def test_combine_different_models(user_query, another_user_query):
    another_query = Query(User)
    with pytest.raises(TypeError):
        user_query.combine(another_query, Q)

def test_combine_sliced_query(user_query, another_user_query):
    user_query.set_limits(0, 10)
    with pytest.raises(TypeError):
        user_query.combine(another_user_query, Q)

def test_combine_different_distincts(user_query, another_user_query):
    user_query.distinct = True
    another_user_query.distinct = False
    with pytest.raises(TypeError):
        user_query.combine(another_user_query, Q)

def test_combine_different_distinct_fields(user_query, another_user_query):
    user_query.distinct_fields = ['username']
    another_user_query.distinct_fields = ['email']
    with pytest.raises(TypeError):
        user_query.combine(another_user_query, Q)

def test_combine_properly(user_query, another_user_query):
    combined_query = user_query.combine(another_user_query, Q)
    assert combined_query is not None  # Ensure combined_query is valid
    assert isinstance(combined_query, Query)  # Ensure the result is still a Query instance

def test_combine_with_and(user_query, another_user_query):
    combined_query = user_query.combine(another_user_query, Q.AND)
    assert combined_query.where.connector == Q.AND  # Check if combined query has AND condition

def test_combine_with_or(user_query, another_user_query):
    combined_query = user_query.combine(another_user_query, Q.OR)
    assert combined_query.where.connector == Q.OR  # Check if combined query has OR condition

def test_combine_with_extra(user_query, another_user_query):
    user_query.extra = {'select': ['extra_field']}
    another_user_query.extra = {'select': ['another_field']}
    combined_query = user_query.combine(another_user_query, Q.AND)
    assert len(combined_query.extra) == 2  # Ensure extra fields are combined properly