import pytest
from django.contrib.auth.models import User
from django.db.models import Aggregate, FloatField
from django.db import connection
from django.db.backends.sqlite3.base import list_aggregate

def test_list_aggregate():
    # Define a custom aggregate function using the `list_aggregate` function
    class CollectList(list_aggregate(lambda x: x)):
        def __init__(self):
            super().__init__()

    # Create a sample user to test with
    User.objects.create(username='test_user', email='test@example.com')

    # Perform the aggregate on the User model
    aggregate_result = User.objects.aggregate(collect_users=CollectList())

    # Check that the result is a list and contains the username of the test user
    assert isinstance(aggregate_result['collect_users'], list)
    assert 'test_user' in aggregate_result['collect_users']

    # Test with a multi-user scenario
    User.objects.create(username='another_user', email='another@example.com')
    aggregate_result = User.objects.aggregate(collect_users=CollectList())

    # Check that the result includes both users
    assert isinstance(aggregate_result['collect_users'], list)
    assert 'test_user' in aggregate_result['collect_users']
    assert 'another_user' in aggregate_result['collect_users']

    # Test finalization by checking if it can handle applying final function
    final_result = aggregate_result['collect_users'].finalize()
    assert final_result == aggregate_result['collect_users']  # This will depend on your final function logic