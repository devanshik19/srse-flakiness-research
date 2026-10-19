import pytest
from django.db.models import Sum, Count
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

@pytest.fixture
def user_queryset():
    return User.objects.annotate(total_users=Count('id')).values()

def test_get_aggregation_no_annotations(user_queryset):
    query = Query(User)
    result = query.get_aggregation(using=DEFAULT_DB_ALIAS, added_aggregate_names=set())
    assert result == {}

def test_get_aggregation_with_annotations(user_queryset):
    query = Query(User).annotate(total_users=Count('id'))
    result = query.get_aggregation(using=DEFAULT_DB_ALIAS, added_aggregate_names={'total_users'})
    assert result['total_users'] == [User.objects.count()]

def test_get_aggregation_with_slicing(user_queryset):
    query = Query(User).annotate(total_users=Count('id'))[0:5]
    result = query.get_aggregation(using=DEFAULT_DB_ALIAS, added_aggregate_names={'total_users'})
    assert result['total_users'] == [User.objects.count()]

def test_get_aggregation_with_distinct(user_queryset):
    query = Query(User).distinct().annotate(total_users=Count('id'))
    result = query.get_aggregation(using=DEFAULT_DB_ALIAS, added_aggregate_names={'total_users'})
    assert result['total_users'] == [User.objects.distinct().count()]

def test_get_aggregation_with_group_by(user_queryset):
    query = Query(User).values('username').annotate(total_users=Count('id'))
    result = query.get_aggregation(using=DEFAULT_DB_ALIAS, added_aggregate_names={'total_users'})
    assert result['total_users'] == [User.objects.values('username').count()]