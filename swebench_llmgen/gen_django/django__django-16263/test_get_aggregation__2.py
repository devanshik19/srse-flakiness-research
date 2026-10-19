import pytest
from django.contrib.auth.models import User
from django.db.models import Sum, Count
from django.db.models.sql.query import Query

@pytest.fixture
def user_query():
    # Create a sample User table with some data
    User.objects.create(username='user1', email='user1@example.com')
    User.objects.create(username='user2', email='user2@example.com')
    # Generate a Query object for the User model
    query = Query(User)
    return query

def test_get_aggregation_with_no_annotations(user_query):
    # Test with no existing annotations
    result = user_query.get_aggregation(using='default', added_aggregate_names=[])
    assert result == {}

def test_get_aggregation_with_sum_annotation(user_query):
    # Set up annotations
    user_query.annotations = {'total_users': Count('id')}
    user_query.annotation_select = ['total_users']
    
    # Test aggregation
    result = user_query.get_aggregation(using='default', added_aggregate_names=[])
    assert result['total_users'] == 2

def test_get_aggregation_with_existing_annotation(user_query):
    # Add an existing annotation
    user_query.annotations = {'total_users': Count('id')}
    user_query.annotation_select = ['total_users']
    
    # Added aggregate names should be considered
    result = user_query.get_aggregation(using='default', added_aggregate_names=['total_users'])
    assert result['total_users'] == 2

def test_get_aggregation_with_sliced_query(user_query):
    user_query.is_sliced = True  # Simulate a sliced query
    user_query.annotations = {'total_users': Count('id')}
    user_query.annotation_select = ['total_users']
    
    result = user_query.get_aggregation(using='default', added_aggregate_names=[])
    assert result['total_users'] == 2

def test_get_aggregation_with_distinct(user_query):
    user_query.distinct = True  # Simulate a distinct query
    user_query.annotations = {'total_users': Count('id')}
    user_query.annotation_select = ['total_users']
    
    result = user_query.get_aggregation(using='default', added_aggregate_names=[])
    assert result['total_users'] == 2