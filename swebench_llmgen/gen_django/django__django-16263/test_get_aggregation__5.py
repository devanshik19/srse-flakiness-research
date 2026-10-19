import pytest
from django.contrib.auth.models import User
from django.db.models import Count
from django.db.models.sql.query import Query

@pytest.fixture
def user_query():
    user_queryset = User.objects.annotate(user_count=Count('id'))
    return user_queryset.query

def test_get_aggregation_no_annotations(user_query):
    query = Query(User)
    result = query.get_aggregation(using=DEFAULT_DB_ALIAS, added_aggregate_names=())
    assert result == {}

def test_get_aggregation_with_existing_annotations(user_query):
    query = user_query.clone()
    query.annotations = {'user_count': Count('id')}
    query.annotation_select = ('user_count',)
    added_aggregate_names = ('user_count',)
    
    result = query.get_aggregation(using=DEFAULT_DB_ALIAS, added_aggregate_names=added_aggregate_names)
    assert result == {'user_count': 1}  # Assuming there is at least one User

def test_get_aggregation_with_distinct(user_query):
    query = user_query.clone()
    query.distinct = True
    query.annotations = {'user_count': Count('id')}
    query.annotation_select = ('user_count',)
    added_aggregate_names = ()

    result = query.get_aggregation(using=DEFAULT_DB_ALIAS, added_aggregate_names=added_aggregate_names)
    assert result['user_count'] >= 1  # Should be 1 or more if there are users

def test_get_aggregation_with_group_by(user_query):
    query = user_query.clone()
    query.group_by = ('username',)
    query.annotations = {'user_count': Count('id')}
    query.annotation_select = ('user_count',)
    added_aggregate_names = ()

    result = query.get_aggregation(using=DEFAULT_DB_ALIAS, added_aggregate_names=added_aggregate_names)
    assert isinstance(result, dict)  # Expecting a dict return type
    assert 'user_count' in result  # Should contain the user_count key