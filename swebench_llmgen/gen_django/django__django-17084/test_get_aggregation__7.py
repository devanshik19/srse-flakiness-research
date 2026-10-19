import pytest
from django.db.models import Count
from django.contrib.auth.models import User
from django.db.models.sql.query import Query

@pytest.fixture
def user_query():
    # Create some user instances for testing
    User.objects.create(username='user1')
    User.objects.create(username='user2')
    return Query(User)

def test_get_aggregation_empty_aggregate_exprs(user_query):
    result = user_query.get_aggregation(using='default', aggregate_exprs={})
    assert result == {}

def test_get_aggregation_single_user_count(user_query):
    aggregate_exprs = {
        'user_count': Count('id'),
    }
    result = user_query.get_aggregation(using='default', aggregate_exprs=aggregate_exprs)
    assert result['user_count'] == User.objects.count()

def test_get_aggregation_multiple_aggregations(user_query):
    aggregate_exprs = {
        'user_count': Count('id'),
    }
    user_query.get_aggregation(using='default', aggregate_exprs=aggregate_exprs)
    
    # Now, let's add an aggregation that contains an aggregation
    aggregate_exprs['user_count'] = Count('id')
    result = user_query.get_aggregation(using='default', aggregate_exprs=aggregate_exprs)

    # Verify that the aggregation result is correct
    assert result['user_count'] == User.objects.count()

def test_get_aggregation_with_existing_annotations(user_query):
    # Simulate existing annotations
    user_query.annotations = {
        'existing_annotation': Count('id'),
    }
  
    aggregate_exprs = {
        'new_user_count': Count('id'),
    }
    
    result = user_query.get_aggregation(using='default', aggregate_exprs=aggregate_exprs)
    
    # Validate the result of the aggregation
    assert result['new_user_count'] == User.objects.count()
    # Validate that existing annotations are not replaced
    assert 'existing_annotation' in user_query.annotations

def test_get_aggregation_with_complex_aggregation(user_query):
    aggregate_exprs = {
        'user_count': Count('id'),
    }
    
    user_query = user_query.clone()
    user_query.is_sliced = True  # Simulate slicing
    
    result = user_query.get_aggregation(using='default', aggregate_exprs=aggregate_exprs)
    
    assert result['user_count'] == User.objects.count()