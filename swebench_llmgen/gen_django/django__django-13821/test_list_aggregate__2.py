import pytest
from django.db.models import Aggregate, IntegerField
from django.contrib.auth.models import User
from django.db import connection
from django.db.models import Sum
from django.db.backends.sqlite3.base import list_aggregate

class CustomSum(Aggregate):
    """
    Custom aggregate class to demonstrate list_aggregate with a sum function.
    """
    def __init__(self, *expressions, **extra):
        super().__init__(*expressions, **extra)
        self.function = 'SUM'

@pytest.fixture
def create_users():
    User.objects.create(username='user1', age=25)
    User.objects.create(username='user2', age=30)
    User.objects.create(username='user3', age=35)

def test_list_aggregate(create_users):
    # Testing the custom aggregate with a sum function
    aggregate_class = list_aggregate(Sum)
    users = User.objects.all()
    
    # Using the aggregate to sum the ages of users
    aggregate_instance = aggregate_class()
    for user in users:
        aggregate_instance.step(user.age)

    # Finalizing the result
    result = aggregate_instance.finalize()
    
    # Expected result
    expected_result = sum([user.age for user in users])
    
    assert result == expected_result