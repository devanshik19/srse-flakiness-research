import pytest
from django.contrib.auth.models import User
from django.db.models import Q
from django.db.models.sql.query import Query

@pytest.fixture
def user_query():
    return Query(User)

@pytest.fixture
def other_user_query():
    return Query(User)

def test_combine_different_models(user_query, other_user_query):
    different_model_query = Query(User)  # This will be the same model
    with pytest.raises(TypeError):
        user_query.combine(different_model_query, Q.AND)

def test_combine_sliced_queries(user_query, other_user_query):
    user_query.is_sliced = True  # Simulate that the query is sliced
    with pytest.raises(TypeError):
        user_query.combine(other_user_query, Q.AND)

def test_combine_different_distinct(user_query, other_user_query):
    other_user_query.distinct = True  # Make them distinct
    with pytest.raises(TypeError):
        user_query.combine(other_user_query, Q.AND)

def test_combine_different_distinct_fields(user_query, other_user_query):
    user_query.distinct_fields = ['field1']
    other_user_query.distinct_fields = ['field2']
    with pytest.raises(TypeError):
        user_query.combine(other_user_query, Q.AND)

def test_combine_and_queries(user_query, other_user_query):
    combined_query = user_query.combine(other_user_query, Q.AND)
    assert isinstance(combined_query, Query)
    assert combined_query.where is not None  # Assuming where is expected to be populated

def test_combine_or_queries(user_query, other_user_query):
    combined_query = user_query.combine(other_user_query, Q.OR)
    assert isinstance(combined_query, Query)
    
    with pytest.raises(ValueError):
        user_query.extra = {'select': 'something'}
        other_user_query.extra = {'select': 'something_else'}
        user_query.combine(other_user_query, Q.OR)

def test_combine_updates_ordering(user_query, other_user_query):
    user_query.order_by = ['username']
    other_user_query.order_by = ['email']
    combined_query = user_query.combine(other_user_query, Q.AND)
    assert combined_query.order_by == user_query.order_by  # Checks that current ordering is maintained

def test_combine_updates_extra(user_query, other_user_query):
    user_query.extra = {'select': 'my_field'}
    other_user_query.extra = {'select': 'other_field'}
    combined_query = user_query.combine(other_user_query, Q.AND)
    assert combined_query.extra['select'] == 'my_field'  # Checks that extra is updated correctly