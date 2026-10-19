import pytest
from django.contrib.auth.models import User
from django.db.models import Avg, Count
from django.db.models.sql.query import Query

@pytest.fixture
def user_query():
    # Create some User instances for testing
    User.objects.create(username='user1', email='user1@example.com')
    User.objects.create(username='user2', email='user2@example.com')
    return User.objects.all()

def test_get_aggregation_no_annotations(user_query):
    query = Query(User)
    result = query.get_aggregation(using='default', added_aggregate_names=set())
    assert result == {}

def test_get_aggregation_with_annotations(user_query):
    query = Query(User)
    query.annotations = {
        'count': Count('id'),
        'avg_age': Avg('date_joined')  # Assuming we have some date_joined field
    }
    query.annotation_select = ['count', 'avg_age']
    result = query.get_aggregation(using='default', added_aggregate_names=set())
    assert 'count' in result
    assert 'avg_age' in result

def test_get_aggregation_with_existing_annotations(user_query):
    query = Query(User)
    query.annotations = {
        'count': Count('id'),
        'avg_age': Avg('date_joined'),
    }
    query.annotation_select = ['count', 'avg_age']
    result = query.get_aggregation(using='default', added_aggregate_names={'avg_age'})
    assert 'count' in result
    assert 'avg_age' not in result  # avg_age is excluded

def test_get_aggregation_with_distinct(user_query):
    query = Query(User)
    query.annotations = {
        'count': Count('id'),
    }
    query.annotation_select = ['count']
    query.distinct = True  # Simulating using distinct
    result = query.get_aggregation(using='default', added_aggregate_names=set())
    assert 'count' in result

def test_get_aggregation_with_group_by(user_query):
    query = Query(User)
    query.annotations = {
        'count': Count('id'),
    }
    query.annotation_select = ['count']
    query.group_by = ('username',)  # Simulating a GROUP BY scenario
    result = query.get_aggregation(using='default', added_aggregate_names=set())
    assert 'count' in result