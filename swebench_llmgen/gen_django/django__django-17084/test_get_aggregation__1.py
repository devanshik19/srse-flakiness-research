import pytest
from django.contrib.auth.models import User
from django.db.models import Sum, Avg
from django.db.models.sql.query import Query

@pytest.mark.django_db
def test_get_aggregation():
    # Create test data
    User.objects.create(username='user1', email='user1@example.com')
    User.objects.create(username='user2', email='user2@example.com')
    User.objects.create(username='user3', email='user3@example.com')

    # Create a query instance
    query = Query(User)

    # Define aggregation expressions
    aggregate_exprs = {
        'total_users': Count('id'),
        'avg_username_length': Avg('username')
    }

    # Get aggregation results
    result = query.get_aggregation(DEFAULT_DB_ALIAS, aggregate_exprs)

    # Assertions to check the outcome
    assert 'total_users' in result
    assert result['total_users'] == 3  # Expecting 3 users
    assert 'avg_username_length' in result
    assert isinstance(result['avg_username_length'], float)  # Ensure the result is a float