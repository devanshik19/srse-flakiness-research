import pytest
from django.db.models import Count
from django.contrib.auth.models import User
from django.db.models.sql.query import Query


def test_get_aggregation_no_annotations():
    query = Query(model=User, alias_cols=())
    result = query.get_aggregation(using='default', added_aggregate_names=set())
    assert result == {}


def test_get_aggregation_with_annotations():
    query = Query(model=User, alias_cols=())
    query.annotations = {
        'user_count': Count('id'),
    }
    query.annotation_select = ['user_count']
    query.default_cols = True

    result = query.get_aggregation(using='default', added_aggregate_names=set())
    assert result['user_count'] == 0  # Initially, with no users, count should be 0.


def test_get_aggregation_with_existing_annotations():
    query = Query(model=User, alias_cols=())
    query.annotations = {
        'user_count': Count('id'),
        'another_annotation': Count('username'),
    }
    query.annotation_select = ['user_count', 'another_annotation']
    query.group_by = ('username',)
    query.is_sliced = False
    query.distinct = False

    result = query.get_aggregation(using='default', added_aggregate_names={'another_annotation'})
    assert 'another_annotation' not in result  # should not include removed annotation
    assert result['user_count'] == 0  # Still count should be 0.


def test_get_aggregation_with_subquery():
    query = Query(model=User, alias_cols=())
    query.annotations = {
        'user_count': Count('id'),
    }
    query.annotation_select = ['user_count']
    query.group_by = ('username',)  # Forces subquery.
    query.is_sliced = True  # Simulate slicing.

    result = query.get_aggregation(using='default', added_aggregate_names=set())
    assert result['user_count'] == 0  # Count should still be 0.