import pytest
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

def test_get_aggregation_no_annotations():
    user = User.objects.create(username='test_user')
    query = Query(model=User, alias_cols=())
    result = query.get_aggregation(using=DEFAULT_DB_ALIAS, added_aggregate_names=set())
    assert result == {}

def test_get_aggregation_with_annotations():
    user = User.objects.create(username='test_user')
    query = Query(model=User, alias_cols=())
    query.annotations = {'count_users': Count('id')}
    query.annotation_select = ['count_users']

    result = query.get_aggregation(using=DEFAULT_DB_ALIAS, added_aggregate_names=set())
    assert result == {'count_users': 1}

def test_get_aggregation_with_existing_annotations():
    user = User.objects.create(username='test_user')
    query = Query(model=User, alias_cols=())
    query.annotations = {'count_users': Count('id')}
    query.annotation_select = ['count_users']
    added_aggregate_names = {'count_users'}

    result = query.get_aggregation(using=DEFAULT_DB_ALIAS, added_aggregate_names=added_aggregate_names)
    assert result == {'count_users': 1}

def test_get_aggregation_with_slicing():
    user1 = User.objects.create(username='test_user1')
    user2 = User.objects.create(username='test_user2')
    query = Query(model=User, alias_cols=())
    query.annotations = {'count_users': Count('id')}
    query.annotation_select = ['count_users']
    query.is_sliced = True
    
    result = query.get_aggregation(using=DEFAULT_DB_ALIAS, added_aggregate_names=set())
    assert result == {'count_users': 2}

def test_get_aggregation_with_distinct():
    user1 = User.objects.create(username='test_user1')
    user2 = User.objects.create(username='test_user2')
    query = Query(model=User, alias_cols=())
    query.annotations = {'count_users': Count('id')}
    query.annotation_select = ['count_users']
    query.distinct = True
    
    result = query.get_aggregation(using=DEFAULT_DB_ALIAS, added_aggregate_names=set())
    assert result == {'count_users': 2}

def test_get_aggregation_with_empty_result_value():
    user = User.objects.create(username='test_user')
    query = Query(model=User, alias_cols=())
    query.annotations = {'count_users': Count('id')}
    query.annotation_select = ['count_users']
    query.select = ()
    query.default_cols = False
    
    result = query.get_aggregation(using=DEFAULT_DB_ALIAS, added_aggregate_names=set())
    assert result == {'count_users': 1}