import pytest
from django.db.models import Sum
from django.contrib.auth.models import User
from django.db import connection
from django.db.models.sql.query import Query

@pytest.fixture
def user_queryset():
    # Creating two User instances for testing
    User.objects.create(username='user1', email='user1@example.com')
    User.objects.create(username='user2', email='user2@example.com')
    return User.objects.all()

def test_get_aggregation_no_annotations(user_queryset):
    query = Query(User)
    result = query.get_aggregation(using=connection.alias, added_aggregate_names=[])
    assert result == {}

def test_get_aggregation_with_annotations(user_queryset):
    query = Query(User)
    query.annotations['total_users'] = Sum('id')
    query.annotation_select = ['total_users']
    
    result = query.get_aggregation(using=connection.alias, added_aggregate_names=[])
    assert 'total_users' in result
    assert result['total_users'] == 3  # 1+2 from the created user instances

def test_get_aggregation_with_added_aggregate_names(user_queryset):
    query = Query(User)
    query.annotations['total_users'] = Sum('id')
    query.annotation_select = ['total_users']
    
    # Simulating that 'total_users' has been added previously
    added_aggregate_names = ['total_users']
    
    result = query.get_aggregation(using=connection.alias, added_aggregate_names=added_aggregate_names)
    assert result == {}

def test_get_aggregation_with_existing_annotations(user_queryset):
    query = Query(User)
    query.annotations['total_users'] = Sum('id')
    query.annotation_select = ['total_users', 'existing_annotation']
    
    query.annotations['existing_annotation'] = Sum('id')  # Some extra annotation
    added_aggregate_names = ['existing_annotation']
    
    result = query.get_aggregation(using=connection.alias, added_aggregate_names=added_aggregate_names)
    assert 'total_users' in result
    assert result['total_users'] == 3

def test_get_aggregation_with_group_by(user_queryset):
    query = Query(User)
    query.annotations['count_users'] = Sum('id')
    query.annotation_select = ['count_users']
    query.group_by = ('id',)  # Simulate a group by scenario
    
    result = query.get_aggregation(using=connection.alias, added_aggregate_names=[])
    assert 'count_users' in result
    assert result['count_users'] == 3