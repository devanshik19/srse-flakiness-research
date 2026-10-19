import pytest
from django.contrib.auth.models import User
from django.db.models import Sum, Count
from django.db.models.sql.query import Query

@pytest.fixture
def user_instance():
    return User.objects.create(username='testuser', email='test@example.com')

def test_get_aggregation_with_valid_aggregate(user_instance):
    query = Query(User)
    aggregate_exprs = {
        'total_users': Count('id'),
        'email_count': Count('email')
    }
    
    result = query.get_aggregation(using='default', aggregate_exprs=aggregate_exprs)

    assert result == {
        'total_users': 1,  # As one user is created in the fixture
        'email_count': 1   # The created user has an email
    }

def test_get_aggregation_with_empty_exprs():
    query = Query(User)
    result = query.get_aggregation(using='default', aggregate_exprs={})

    assert result == {}

def test_get_aggregation_with_non_aggregate_expression(user_instance):
    query = Query(User)
    aggregate_exprs = {
        'username_invalid': user_instance.username  # Invalid usage
    }
    
    with pytest.raises(TypeError) as excinfo:
        query.get_aggregation(using='default', aggregate_exprs=aggregate_exprs)
        
    assert str(excinfo.value) == "username_invalid is not an aggregate expression"

def test_get_aggregation_with_aggregation_and_filters(user_instance):
    query = Query(User)
    aggregate_exprs = {
        'total_users': Count('id'),
    }
    
    # Simulate adding a filter
    query.where = 'username = %s'
    query.params = [user_instance.username]

    result = query.get_aggregation(using='default', aggregate_exprs=aggregate_exprs)

    assert result == {
        'total_users': 1  # Still the same as we filtered using the username
    }

def test_get_aggregation_with_multiple_aggregates(user_instance):
    query = Query(User)
    aggregate_exprs = {
        'total_users': Count('id'),
        'email_count': Count('email')
    }
    
    # Creating a second user to test multiple aggregations
    User.objects.create(username='testuser2', email='test2@example.com')

    result = query.get_aggregation(using='default', aggregate_exprs=aggregate_exprs)

    assert result == {
        'total_users': 2,  # Two users created
        'email_count': 2    # Both users have emails
    }