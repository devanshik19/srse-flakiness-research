import pytest
from django.contrib.auth.models import User
from django.db.models import Sum, Count
from django.db.models.sql.query import Query

@pytest.mark.parametrize("aggregate_exprs, expected_result", [
    ({
        'total_age': Sum('age'),
    }, {'total_age': None}),
    ({
        'user_count': Count('id'),
    }, {'user_count': 0}),
])
def test_get_aggregation(aggregate_exprs, expected_result):
    # Arrange: Create some test users
    User.objects.create(username='user1', age=30)
    User.objects.create(username='user2', age=25)
    
    # Act: Create an instance of Query for User model
    query = Query(User)
    
    # Calling the method under test
    result = query.get_aggregation(using='default', aggregate_exprs=aggregate_exprs)

    # Assert: Validate the result against expected
    assert result == expected_result

def test_get_aggregation_with_existing_annotations():
    # Arrange: Create users and add annotations
    User.objects.create(username='user1', age=30)
    User.objects.create(username='user2', age=25)

    # Prepare a custom Query object
    query = Query(User)
    
    # Set an initial annotation
    query.annotations['initial_count'] = Count('id')
    
    aggregate_exprs = {
        'total_age': Sum('age'),
        'user_count': Count('id'),
    }

    # Act: Call get_aggregation
    result = query.get_aggregation(using='default', aggregate_exprs=aggregate_exprs)

    # Assert: Validate that the aggregation includes the annotations
    assert 'total_age' in result
    assert 'user_count' in result
    assert (result['total_age'] in (30, 55))  # Expecting the sum of ages
    assert result['user_count'] == 2  # Counting the number of users