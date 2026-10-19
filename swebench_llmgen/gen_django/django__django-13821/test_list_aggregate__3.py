import pytest
from django.contrib.auth.models import User
from django.db.backends.sqlite3.base import list_aggregate

def test_list_aggregate():
    # Define a simple function to be used as the finalize method.
    def finalize(values):
        return sum(values)

    # Create the aggregate class using the list_aggregate function.
    ListAggregate = list_aggregate(finalize)

    # Test the step method (which is list.append).
    aggregate_instance = ListAggregate()
    assert isinstance(aggregate_instance, list)

    # Append some values to the aggregate.
    aggregate_instance.step(10)
    aggregate_instance.step(20)
    aggregate_instance.step(30)

    # Test the finalize method.
    result = aggregate_instance.finalize(aggregate_instance)
    assert result == 60  # 10 + 20 + 30
    
    # Test with an empty list.
    empty_aggregate_instance = ListAggregate()
    result_empty = empty_aggregate_instance.finalize(empty_aggregate_instance)
    assert result_empty == 0  # sum of an empty list should be 0
    
    # Ensure that the original method works with User instances.
    user_1 = User.objects.create_user(username='user1', password='password')
    user_2 = User.objects.create_user(username='user2', password='password')

    # Use a custom finalize function to count the number of created users
    def count_users(user_list):
        return len(user_list)

    UserAggregate = list_aggregate(count_users)
    user_aggregate_instance = UserAggregate()
    
    # Add User instances to the aggregate.
    user_aggregate_instance.step(user_1)
    user_aggregate_instance.step(user_2)

    total_users = user_aggregate_instance.finalize(user_aggregate_instance)
    assert total_users == 2  # Should be 2 users added.