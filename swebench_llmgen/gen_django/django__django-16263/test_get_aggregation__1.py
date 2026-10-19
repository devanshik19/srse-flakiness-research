import pytest
from django.contrib.auth.models import User
from django.db.models import Count
from django.db.models.sql.query import Query

@pytest.mark.django_db
def test_get_aggregation_no_annotations():
    query = Query(User)
    result = query.get_aggregation(using='default', added_aggregate_names=[])
    assert result == {}

@pytest.mark.django_db
def test_get_aggregation_with_annotations():
    query = Query(User)
    query.annotations = {
        'active_count': Count('id'),
    }
    query.annotation_select = ['active_count']
    result = query.get_aggregation(using='default', added_aggregate_names=[])
    assert 'active_count' in result
    assert isinstance(result['active_count'], int)

@pytest.mark.django_db
def test_get_aggregation_with_existing_aggregates():
    query = Query(User)
    query.annotations = {
        'active_count': Count('id'),
        'inactive_count': Count('id', filter=Q(is_active=False)),
    }
    query.annotation_select = ['active_count', 'inactive_count']
    result = query.get_aggregation(using='default', added_aggregate_names=['inactive_count'])
    assert 'active_count' in result
    assert 'inactive_count' not in result
    assert isinstance(result['active_count'], int)

@pytest.mark.django_db
def test_get_aggregation_with_group_by():
    query = Query(User)
    query.annotations = {
        'active_count': Count('id'),
    }
    query.group_by = ('username',)
    query.annotation_select = ['active_count']
    result = query.get_aggregation(using='default', added_aggregate_names=[])
    assert 'active_count' in result
    assert isinstance(result['active_count'], int)

@pytest.mark.django_db
def test_get_aggregation_empty_set_value():
    query = Query(User)
    query.annotations = {
        'user_count': Count('id'),
    }
    query.annotation_select = ['user_count']
    # Manipulate state to force empty result
    query.has_select_fields = False
    result = query.get_aggregation(using='default', added_aggregate_names=[])
    assert 'user_count' in result
    assert result['user_count'] == query.empty_result_set_value