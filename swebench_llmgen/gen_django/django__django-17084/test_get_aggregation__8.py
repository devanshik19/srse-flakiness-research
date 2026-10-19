import pytest
from django.contrib.auth.models import User
from django.db.models import Count
from django.db.models.sql.query import Query

@pytest.fixture
def user_data():
    User.objects.create(username='user1', email='user1@example.com')
    User.objects.create(username='user2', email='user2@example.com')

def test_get_aggregation_with_aggregation(user_data):
    query = Query(User)
    aggregate_exprs = {
        'user_count': Count('id')
    }
    result = query.get_aggregation(using='default', aggregate_exprs=aggregate_exprs)
    assert result['user_count'] == 2, "Expected user count to be 2"

def test_get_aggregation_no_aggregation(user_data):
    query = Query(User)
    result = query.get_aggregation(using='default', aggregate_exprs={})
    assert result == {}, "Expected an empty result for no aggregation"

def test_get_aggregation_invalid_aggregate(user_data):
    query = Query(User)
    aggregate_exprs = {
        'invalid_aggregate': Count('username')  # Note: This is a valid Count. Testing error handling for expectations
    }

    with pytest.raises(TypeError, match='invalid_aggregate is not an aggregate expression'):
        query.get_aggregation(using='default', aggregate_exprs=aggregate_exprs)