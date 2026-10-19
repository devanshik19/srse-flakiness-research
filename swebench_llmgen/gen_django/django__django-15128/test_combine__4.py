import pytest
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.sql.query import Query

@pytest.fixture
def user_query():
    return User.objects.all()

def test_combine_type_error_different_models(user_query):
    with pytest.raises(TypeError):
        query1 = Query(User)
        query2 = Query(User)
        query1.combine(query2, 'AND')

def test_combine_type_error_sliced_query(user_query):
    query1 = user_query[:5]
    query2 = user_query
    with pytest.raises(TypeError):
        query1.combine(query2, 'AND')

def test_combine_type_error_distinct_queries(user_query):
    query1 = user_query.distinct()
    query2 = user_query.distinct()
    with pytest.raises(TypeError):
        query1.combine(query2, 'AND')

def test_combine_type_error_different_distinct_fields(user_query):
    query1 = user_query.distinct('id')
    query2 = user_query.distinct('username')
    with pytest.raises(TypeError):
        query1.combine(query2, 'AND')

def test_combine_and_queries(user_query):
    query1 = user_query.filter(Q(is_active=True))
    query2 = user_query.filter(Q(is_staff=True))
    combined = query1.combine(query2, 'AND')
    assert combined.query.where == query1.query.where + query2.query.where

def test_combine_or_queries(user_query):
    query1 = user_query.filter(Q(is_active=True))
    query2 = user_query.filter(Q(is_staff=True))
    combined = query1.combine(query2, 'OR')
    assert combined.query.where == query1.query.where + query2.query.where

def test_combine_extra_select(user_query):
    query1 = user_query.extra(select={'custom_field': 'username'})
    query2 = user_query.extra(select={'another_field': 'email'})
    combined = query1.combine(query2, 'AND')
    assert combined.query.extra == {**query1.query.extra, **query2.query.extra}

def test_combine_order_by(user_query):
    query1 = user_query.order_by('username')
    query2 = user_query.order_by('email')
    combined = query1.combine(query2, 'AND')
    assert combined.query.order_by == query2.query.order_by