import pytest
from django.db.models import Sum, Count
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

def test_get_aggregation_with_no_annotations():
    query = Query(User)
    result = query.get_aggregation(using=DEFAULT_DB_ALIAS, added_aggregate_names=set())
    assert result == {}

def test_get_aggregation_with_annotations():
    query = Query(User)
    query.annotations = {'total_users': Count('id')}
    query.annotation_select = ['total_users']
    result = query.get_aggregation(using=DEFAULT_DB_ALIAS, added_aggregate_names=set())
    assert 'total_users' in result
    assert result['total_users'] == User.objects.count()

def test_get_aggregation_with_existing_annotations():
    query = Query(User)
    query.annotations = {'total_users': Count('id')}
    query.annotation_select = ['total_users']
    added_aggregate_names = {'total_users'}
    result = query.get_aggregation(using=DEFAULT_DB_ALIAS, added_aggregate_names=added_aggregate_names)
    assert 'total_users' not in result

def test_get_aggregation_with_group_by():
    query = Query(User)
    query.group_by = ('username',)
    query.annotations = {'total_users': Count('id')}
    query.annotation_select = ['total_users']
    result = query.get_aggregation(using=DEFAULT_DB_ALIAS, added_aggregate_names=set())
    assert 'total_users' in result