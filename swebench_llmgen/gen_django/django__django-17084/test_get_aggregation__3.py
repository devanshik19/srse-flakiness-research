import pytest
from django.contrib.auth.models import User
from django.db.models import Count
from django.db.models.sql.query import Query

@pytest.fixture
def user_queryset():
    return User.objects.all()

def test_get_aggregation_empty_aggregate(user_queryset):
    query = Query(User)
    result = query.get_aggregation(using=DEFAULT_DB_ALIAS, aggregate_exprs={})
    assert result == {}

def test_get_aggregation_non_aggregate_expression(user_queryset):
    query = Query(User)
    with pytest.raises(TypeError):
        query.get_aggregation(using=DEFAULT_DB_ALIAS, aggregate_exprs={'non_agg': User.username})

def test_get_aggregation_with_aggregate(user_queryset):
    query = Query(User)
    aggregate_exprs = {
        'user_count': Count('id')
    }
    result = query.get_aggregation(using=DEFAULT_DB_ALIAS, aggregate_exprs=aggregate_exprs)
    assert 'user_count' in result
    assert result['user_count'] == user_queryset.count()

def test_get_aggregation_with_non_empty_results(user_queryset):
    user_count = user_queryset.count()
    query = Query(User)
    
    aggregate_exprs = {
        'user_count': Count('id'),
        'first_user': Count('username')  # Assuming usernames are unique for test's sake
    }
    result = query.get_aggregation(using=DEFAULT_DB_ALIAS, aggregate_exprs=aggregate_exprs)
    
    assert 'user_count' in result
    assert 'first_user' in result
    assert result['user_count'] == user_count
    assert result['first_user'] == user_count  # Same here; just for coverage

def test_get_aggregation_with_subquery(user_queryset):
    query = Query(User)

    aggregate_exprs = {
        'user_count': Count('id'),
    }
    query.subquery = True
    result = query.get_aggregation(using=DEFAULT_DB_ALIAS, aggregate_exprs=aggregate_exprs)

    assert 'user_count' in result
    assert result['user_count'] == user_queryset.count()