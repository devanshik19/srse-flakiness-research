import pytest
from django.contrib.auth.models import User
from django.db import connection

def test_list_aggregate():
    # Aggregate function to compute length
    def finalize_func(lst):
        return len(lst)

    # Create an aggregate using list_aggregate
    ListAggregate = list_aggregate(finalize_func)

    # Prepare data for testing the aggregate
    user1 = User.objects.create(username='user1')
    user2 = User.objects.create(username='user2')
    
    # Use the custom aggregate in a raw SQL query
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT list_aggregate(username) AS usernames FROM auth_user"
        )
        result = cursor.fetchone()

    # Verify the result
    aggregate_result = result[0]
    expected_result = 2  # We have created two users
    assert aggregate_result == expected_result

    # Test finalize with an empty list
    empty_aggregate = ListAggregate()
    assert finalize_func(empty_aggregate) == 0

    # Test with valid data
    filled_aggregate = ListAggregate()
    filled_aggregate.step('user1')
    filled_aggregate.step('user2')
    assert finalize_func(filled_aggregate) == 2